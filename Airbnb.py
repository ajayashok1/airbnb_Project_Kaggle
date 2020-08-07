import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as mpimg
from wordcloud import WordCloud


def get_ingested_data_from_csv():
    data_frame = pd.read_csv('/Users/Ajay/Desktop/AB_NYC_2019.csv')
    data_frame.fillna({'reviews_per_month': 0}, inplace=True)
    return data_frame


def filter_room_data_of_top_neighbourhood_group():
    room_data = airbnb_data.loc[
        airbnb_data['neighbourhood_group'].isin(['Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx'])]
    return room_data


def create_distribution_room_type_plot(room_data):
    room_type_plot_graph = sns.catplot(x='room_type', col='neighbourhood_group',
                                       data=room_data, kind='count',
                                       height=5, aspect=0.7)
    room_type_plot_graph.set_xticklabels(rotation=90)


def get_neighbourhood_group_room_types_average_price():
    room_types_average_price = airbnb_data.groupby(['neighbourhood_group', 'room_type']).agg(
        {'price': 'mean'}).reset_index()
    return room_types_average_price


def room_types():
    rooms_types_available = ['Entire home/apt', 'Private room', 'Shared room']
    return rooms_types_available


def create_plot_neighbourhood_group_room_types_average_price(rooms_types_available, room_types_average_price):
    for room in rooms_types_available:
        sns.lineplot(x='neighbourhood_group', y='price',
                     data=room_types_average_price[
                         room_types_average_price['room_type'] == room],
                     label=room)
    plt.xlabel("Neighbourhood_group", size=13), plt.ylabel("Average price", size=13), plt.title("Neighbourhood_group "
                                                                                                "vs "
                                                                                                "Average Price vs "
                                                                                                "Room_type", size=15,
                                                                                                weight='bold')


def get_airbnb_neighbourhoods_in_neighbourhood_group_average_pricing():
    airbnb_neighbourhoods_in_neighbourhood_group_average_price = airbnb_data.groupby(
        ['neighbourhood_group', 'neighbourhood']).agg({'price': 'min'}).reset_index()
    return airbnb_neighbourhoods_in_neighbourhood_group_average_price


def get_neighbourhood_groups():
    neighbourhood_groups_available = ['Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx']
    return neighbourhood_groups_available


def create_plot_airbnb_neighbourhoods_average_price(neighbourhood_groups_available,
                                                    airbnb_neighbourhoods_in_neighbourhood_group_average_price):
    for ngg_type in neighbourhood_groups_available:
        sns.lineplot(x='neighbourhood', y='price',
                     data=airbnb_neighbourhoods_in_neighbourhood_group_average_price[airbnb_neighbourhoods_in_neighbourhood_group_average_price['neighbourhood_group'] == ngg_type],
                     label=ngg_type)
    plt.figure(figsize=(12, 8))
    sns.set_palette("Set1"), plt.xlabel("Neighbourhood", size=13), plt.ylabel("Average price", size=13), plt.title(
        " Average Price vs Neighbourhood", size=15, weight='bold')


def get_top_5_neighbourhoods_in_each_group():
    neighbourhood_neighbourhood_group_grouped = airbnb_data.groupby(
        ['neighbourhood', 'neighbourhood_group']).agg({'price': 'mean'}).reset_index()
    top_5_niehgbourhoods = neighbourhood_neighbourhood_group_grouped.groupby(
        ["neighbourhood_group"]).apply(lambda x: x.sort_values(["price"], ascending=True)).reset_index(drop=True)
    low_priced_rooms = top_5_niehgbourhoods.groupby('neighbourhood_group').head(5)
    low_priced_rooms.rename(columns={'price': 'avp'})
    return low_priced_rooms


def create_plot_for_five_low_priced_rooms_in_each_neighbourhood_group(value, low_priced_rooms):
    for lp_rooms in value:
        ax = sns.relplot(x='neighbourhood', y='avp', col='neighbourhood_group',
                          data=low_priced_rooms[low_priced_rooms['neighbourhood_group'] == lp_rooms], height=5,
                          aspect=0.7)
        ax.set_xticklabels(rotation=90)


def get_top_5_locations_cheap_expensive(data):
    airbnb_top_5_locations = airbnb_data.groupby(['neighbourhood', 'neighbourhood_group']).agg({'price': 'mean'}).reset_index()
    airbnb_top_5_locations_neighbourhood_group = airbnb_top_5_locations.groupby(["neighbourhood_group"]).apply(lambda x: x.sort_values(["price"], ascending=data)).reset_index(drop=True)
    high_priced_rooms = airbnb_top_5_locations_neighbourhood_group.groupby('neighbourhood_group').head(5)
    high_priced_rooms = high_priced_rooms.rename(columns={'price': 'avp'})
    return high_priced_rooms


def create_plot_for_five_rooms_in_each_neighbourhood_group(value, high_priced_rooms):
    for lp_rooms in value:
        ax = sns.relplot(x='neighbourhood', y='avp', col='neighbourhood_group',
                          data=high_priced_rooms[high_priced_rooms['neighbourhood_group'] == lp_rooms], height=5,
                          aspect=0.7)
        ax.set_xticklabels(rotation=90)


def get_density_check():
    density_chk = airbnb_data[airbnb_data.price < 500]
    density_rooms_plot = sns.violinplot(data=density_chk, x='neighbourhood_group', y='price')
    density_rooms_plot.set_title('Density and distribution of prices for each neighbourhood_group')


def get_wordcloud_for_airbnb(room_price):
    plt.subplots(figsize=(25, 15))
    wordcloud= WordCloud(
        background_color='green',
        width=1800,
        height=1000).generate(" ".join(room_price.neighbourhood))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('neighbourhood.png')
    plt.show()


airbnb_data = get_ingested_data_from_csv()
room_data_of_top_neighbourhood_group = filter_room_data_of_top_neighbourhood_group()
create_distribution_room_type_plot(room_data_of_top_neighbourhood_group)
neighbourhood_group_room_types_average_price = get_neighbourhood_group_room_types_average_price()
room_types_of_neighbourhood_group = room_types()
create_plot_neighbourhood_group_room_types_average_price(room_types_of_neighbourhood_group, neighbourhood_group_room_types_average_price)
neighbourhoods_in_neighbourhood_group_average_price = get_airbnb_neighbourhoods_in_neighbourhood_group_average_pricing()
neighbourhood_groups = get_neighbourhood_groups()
neighbourhood_group_cheap_5_locations = get_top_5_locations_cheap_expensive('true')
create_plot_for_five_rooms_in_each_neighbourhood_group(neighbourhood_groups, neighbourhood_group_cheap_5_locations)
top5_expensive_neighbourhoods_in_each_neighbourhood_group = get_top_5_locations_cheap_expensive('false')
create_plot_for_five_rooms_in_each_neighbourhood_group(neighbourhood_groups, top5_expensive_neighbourhoods_in_each_neighbourhood_group)
get_density_check()
get_wordcloud_for_airbnb(neighbourhood_group_cheap_5_locations)



