'''Formats data from XML into a pandas dataframe'''
#pylint: disable=import-error,E0001
import re
import xml.etree.ElementTree as ET
import logging
import pandas as pd
import spacy as sp
import pycountry as pyc
from rapidfuzz import process,fuzz
from extract import extract_alias


def get_keywords(keyword_list: ET.Element) -> list:
    '''Returns a list of keywords'''
    if keyword_list is not None:
        return [keyword.text for keyword in keyword_list.findall('.//Keyword')]

    return None

def get_mesh_id(mesh_id_list: ET.Element) -> list:
    '''Returns a list of mesh ids'''
    if mesh_id_list is not None:
        return [mesh.find('DescriptorName').attrib.get('UI')
                                for mesh in mesh_id_list.findall('MeshHeading')]

    return None

def transform(data: ET.ElementTree) -> pd.DataFrame:
    '''Loops through the articles and returns article, author and affiliate data'''
    articles_list = []
    counter = 0
    for article in data.findall('.//PubmedArticle'):
        counter += 1
        if counter % 100 == 0:
            logging.info('Data obtained for %s articles',counter)
        article_dict = get_article_data(article)
        for author in article.findall('.//Author'):
            author_dict = get_author_data(article)
            for affiliate in author.findall('.//AffiliationInfo'):
                affiliate_dict = get_affiliation_data(affiliate)
                articles_list.append(article_dict| author_dict | affiliate_dict)
    logging.info('Total number of articles obtained: %s',counter)
    return pd.DataFrame(articles_list)

def get_article_data(article: ET.ElementTree) -> dict:
    '''Returns a pandas dataframe for a given article'''
    article_data = {'pmid': article.findtext('.//PMID'),
                    'title': article.findtext('.//ArticleTitle'),
                    'year': article.findtext('.//PubDate/Year')}

    article_data['keywords'] = get_keywords(article.find('.//KeywordList'))
    article_data['mesh'] = get_mesh_id(article.find('.//MeshHeadingList'))

    return article_data

def get_author_data(author: ET.ElementTree) -> dict:
    '''Returns a list of authors and their affiliations'''
    author_data = {'forename': author.findtext('.//ForeName'),
                   'surname': author.findtext('.//LastName'),
                   'initials': author.findtext('.//Initials'),
                   'fullname':
                    f'{author.findtext('.//ForeName')} {author.findtext('.//LastName')}'
                    }

    return author_data

def get_affiliation_data(affiliate: ET.ElementTree) -> dict:
    '''Returns a dict with the relevant affiliate data'''
    institute_data = {'grid_id': affiliate.findtext(".//Identifier[@Source='GRID']"),
                    'affiliation': affiliate.findtext('.//Affiliation'),
                    'zipcode': get_zipcode(affiliate.findtext('.//Affiliation')),
                    'email': get_author_email(affiliate.findtext('.//Affiliation'))}

    return institute_data

def get_author_email(affiliate: str) -> str:
    '''Uses regex to get the email address'''
    pattern = r'[:.] (\w+|\d+)[@]\w+[.].{0,7}$'
    match = re.search(pattern,affiliate)
    if match:
        return match.group()[1:-1]
    return 'N/A'

def get_zipcode(affiliate: str) -> str:
    '''Uses regex to return the affiliates zipcode'''
    pattern = r' (\w+ \d{5})|(\w{1,2}\d{1,2}\w{0,1} \d\w{2})|(\w\d\w \d\w\d)'
    match = re.search(pattern,affiliate)
    if match:
        return match.group()
    return 'N/A'

def wrangle_data(data: pd.DataFrame) -> pd.DataFrame:
    '''Uses NER and fuzzy matching to return additional affiliate data'''
    nlp = sp.load("en_core_web_md")
    logging.info('Natural language processor loaded successfully.')

    aliases = extract_alias()
    if not aliases.empty:
        logging.info('Aliases extracted successfully.')
        aliases['alias'] = aliases['alias'].str.lower()

        data['country'] = data['affiliation'].apply(lambda x: get_country(x,nlp))
        logging.info('Countries identified for %s/%s rows.', data['country'].count(), len(data))

        data['affiliate_name'] = data['affiliation'].apply(lambda x: get_institute_name(x,nlp))
        logging.info('Affiliations identified for %s/%s rows.',
                     data['affiliate_name'].count(),len(data))

        data[['grid_id', 'GRID_affiliate_name']] = \
        data.apply(lambda row: match_grid_id(row['affiliate_name'], aliases)
                   if pd.isna(row['grid_id'])
                   else map_grid_id(row['grid_id'], aliases), axis=1)
        logging.info('GRID identifiers identified for %s/%s rows.',
                     data['grid_id'].count(), len(data))

    return data


def get_country(affiliate: str, nlp) -> str:
    '''Uses spacy to process the affiliate and return the associated country'''
    countries = [word.text for word in nlp(affiliate).ents
                if word.label_ == 'GPE' and is_country(word.text)]

    if countries:
        return countries[0]

    return None

def is_country(place: str) -> bool:
    '''Checks if a string is a country'''
    try:
        country = pyc.countries.get(name=place)
        return bool(country)
    except LookupError:
        return False

def get_institute_name(institute: str, nlp) -> str:
    '''Uses NER to return the institute name'''
    institute_name = {word.text for word in nlp(institute).ents if word.label_ == "ORG"}

    return [token for token in institute_name if len(token) >= 3 and
            not any(words in token for words in ("Department of", "School of",'Unit'))]

def match_grid_id(affiliates: list, alias_df: pd) -> pd.DataFrame:
    '''Matches GRID ID aliases with the institution name'''
    aliases = alias_df['alias'].tolist()
    for institute in affiliates:
        match,score,index = process.extractOne(institute.lower(),
                            aliases, scorer=fuzz.token_set_ratio,
                            processor=lambda x: x.lower().replace(" ","").replace('"',''))

        if score >= 75:
            return pd.Series([alias_df.iloc[index]['grid_id'],match])
    return pd.Series([None,None])

def map_grid_id(grid_id, alias):
    '''Returns the alias associate with a given grid id'''
    match = alias[alias['grid_id'] == grid_id]
    if not match.empty:
        return pd.Series([grid_id, match.iloc[0]['alias']])
    return pd.Series([grid_id, None])

if __name__ == '__main__':
    transform(ET.ElementTree())
