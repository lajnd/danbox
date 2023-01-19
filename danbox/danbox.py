from googletrans import Translator
from pandas.api.types import CategoricalDtype
import pandas as pd



def create_features(df, label=None):
    """
    Creates time series features from datetime index.
    Parameters:
    df (DataFrame) : DataFrame containing the date time column
    label (str) : column name of the label to be used for time series forecasting, default is None
    
    Returns:
    X (DataFrame) : DataFrame containing the time series features
    y (Series) : pandas Series containing the label, if label is not None
    """

    cat_type = CategoricalDtype(categories=['Monday','Tuesday',
                                            'Wednesday',
                                            'Thursday','Friday',
                                            'Saturday','Sunday'],
                                ordered=True)
    # Copy the input dataframe
    df = df.copy()
    # Create a new column 'date' with the datetime index
    df['date'] = df.index
    # Create new columns for hour, day of week, weekday, quarter, month, year, day of year, day of month, week of year and date offset
    df['hour'] = df['date'].dt.hour
    df['dayofweek'] = df['date'].dt.dayofweek
    df['weekday'] = df['date'].dt.day_name()
    df['weekday'] = df['weekday'].astype(cat_type)
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df['dayofmonth'] = df['date'].dt.day
    df['weekofyear'] = df['date'].dt.isocalendar().weekofyear
    df['date_offset'] = (df.date.dt.month*100 + df.date.dt.day - 320)%1300

    # Create a new column 'season' based on the 'date_offset' column
    df['season'] = pd.cut(df['date_offset'], [0, 300, 602, 900, 1300], labels=['Spring', 'Summer', 'Fall', 'Winter'])
    X = df[['hour','dayofweek','quarter','month','year', 'dayofyear','dayofmonth','weekofyear','weekday','season']]
    if label:
        y = df[label]
        return X, y
    return X



def translate_NL_EN(NL_string):
    """
    Translates a Dutch string to English and replaces all 'and' with '&' and capitalizes the first letter of the sentence
    
    Parameters:
        NL_string (str): A Dutch text that needs to be translated
        
    Returns:
        str : Translated English text with all 'and' replaced with '&' and first letter capitalized.
    """
    # Import the Translator module from the googletrans library
    translator = Translator()
    
    # Translate the NL_string from Dutch to English using the Translator module
    translated = translator.translate(NL_string, dest='en').text
    
    # Replace all instances of "and" with "&" in the translated string
    translated = translated.replace('and', '&')
    
    # Return the translated string with the first letter capitalized
    return translated.capitalize()

