'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import numpy as np 
import re


def get_main_vis_data(stats):
    '''
        Prepare the data for the main visualisation.

        Args:
            stats: The stats dataframe to process
        Returns:
            The data frame to use in the main visualisation
            including the formatted columns index values and price 
            variations and product.
    '''   

    # create a copy of the dataframe
    df = stats.loc[:, ["price","sum_influence_3_days", "index_value", "index_variation", "timestamp", "high_variation"]]

    # Calculate the variation of the index
    df['price_variation'] = df['price'].diff()

    # Rename the 'sum_influence_3_days' column to 'Activity'
    df.rename(columns={'sum_influence_3_days':'Activity'}, inplace=True)

    # Convert scale of the 'Activity' column from units to millions
    df['Activity']=(df['Activity']/1e6).round(1)

    # Round the index value to 2 decimals
    df['index_value']=df['index_value'].round(2)

    # Calculate the product of the price and index variation
    df['product'] = df['price_variation']*df['index_variation']

    return df

def get_bar_chart_data(stats):
    '''
        Prepare the data for the bar chart visualisation.

        Args:
            stats: The stats dataframe to process
        Returns:
            The data frame to use in the bar chart visualisation
            with the formatted columns.
    ''' 
    # Only keep relevant columns
    df = stats.loc[:, ["price","sum_influence_3_days", "index_value", "index_variation"]]

    df['sum_influence_3_days']=(df['sum_influence_3_days']/1e6)

    # Split DF by index variation and range of sum_influence_3_days
    df['variation'] = df['index_variation'].apply(lambda x: 
                                                     'Bearish' if x < -0.025 else (
                                                     'Bullish' if x > 0.025 else 'Neutral'))

    df['sum_influence_3_days'] = pd.cut(df['sum_influence_3_days'], np.arange(0, 19, 2))

    bar_df = df.groupby(['variation', 'sum_influence_3_days']).size().reset_index(name="Count")
    
    # Change format of sum_influence_3_days column from (a, b] to a M - b M
    bar_df['sum_influence_3_days'] = bar_df['sum_influence_3_days'].astype(str).replace(r'\((\d+), (\d+)\]', r'\1 - \2', regex=True)
    return bar_df

def get_radar_trend_data(tweets):
    '''
        From the given tweets dataframe, get
        the average variation for each hour.

        Args:
            df_tweets: The tweets dataframe to process
        Returns:
            The average variation for each hour including columns
            'hour', 'index_variation' and 'hour_angle'.
    '''

    # Only keep relevant columns
    df = tweets.loc[:, ["timestamp", "index_variation"]]

    # Convert the hours from the timestamp
    df['hour'] = df['timestamp'].dt.hour

    # Keep only absolute values reflect movement
    df['index_variation'] = df['index_variation'].abs()

    # Get the average variation for each hour
    df = df.groupby('hour')['index_variation'].mean().reset_index()

    # Convert the hour to an angle
    df['hour_angle'] = df['hour'] * 15

    # Check if there are any missing hours
    missing_hours = [i for i in range(25) if i not in df['hour'].unique()]

    # If there are missing hours, add them to the dataframe
    if 24 in missing_hours and 0 not in missing_hours:
        missing_hours_df = pd.DataFrame({'hour': 0, 
                                         'hour_angle': 0,
                                         'index_variation': df.loc[df['hour'] == 0]['index_variation']})
        df = pd.concat([df, missing_hours_df], ignore_index=True)

    return df

def get_radar_scatter_data(tweets):
    '''
        From the given tweets dataframe, get scatter data
        for each non-negligeable variations per hour.

        Args:
            df_tweets: The tweets dataframe to process
        Returns:
            Scatter dataframe for hour variations including columns
            'hour', 'hour_angle', 'variation' and 'count'.
    '''   

    # Only keep relevant columns
    df = tweets.loc[:, ["timestamp","index_variation"]]

    # Convert the timestamp
    df['hour'] = df['timestamp'].dt.hour
    df['date'] = df['timestamp'].dt.date

    # Keep only absolute values better reflect variation
    df['index_variation'] = df['index_variation'].abs()

    # OPTIONAL : consider only variations greater than 0.1
    df = df.loc[(df['index_variation'] > 0.03)]

    # Regroup by hour and index variation.
    # For instance, values 0.02 and 0.024 will be grouped together.
    # The index variations grouped for each interval of 0.01.
    df['index_range'] = pd.cut(df['index_variation'], bins=[0+i*0.01 for i in range(101)])
    scatter_df = df.groupby(['hour', 'index_range']).size().reset_index(name='count')

    # Convert the hour to an angle
    scatter_df['hour_angle'] = scatter_df['hour'] * 15

    # Give a name to each interval
    scatter_df['variation'] = scatter_df['index_range'].apply(lambda x: x.left)

    # Remove the intervals with no data points
    scatter_df = scatter_df.loc[scatter_df['count'] != 0]
    
    return scatter_df

def convert_dates(df):
    '''
        Converts the dates in the dataframe to datetime objects.
        Creates new columns for the month, day and time.
        
        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with datetime-formatted dates.
    '''
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d').dt.tz_localize(None)
    return df

def select_timeframe(df, start, end):
    '''
        Filters the elements of the dataframe by date, making sure
        they fall in the desired range.

        Args:
            dataframe: The dataframe to process
            start: The starting year (inclusive)
            end: The ending year (inclusive)
        Returns:
            The dataframe filtered by date.
    '''
    df = df[(df['timestamp']<= end ) & (df['timestamp']>= start)]
    return df

def get_timeframe(df):
    '''
        Retrieve the earliest and latest dates in the dataframe.

        Args:
            dataframe: The dataframe to process
        Returns:
            The earliest (start) and latest (end) dates in the dataframe.
    '''
    start = df['timestamp'].min().strftime('%Y-%m-%d')
    end = df['timestamp'].max().strftime('%Y-%m-%d')
    return start,end