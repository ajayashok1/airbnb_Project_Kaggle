import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as mpimg
from wordcloud import WordCloud
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
         host="AJAYs-MacBook-Pro.local",
         user="root",
         password="1234",
         database="AIRBNB"
    )


def get_ingested_data_from_csv():
    data_frame = pd.read_sql("""
                SELECT *
                FROM AIRBNB.ab_nyc_2019
                """, con=mydb)
    data_frame.fillna({'reviews_per_month': 0}, inplace=True)
    return data_frame


def room_types():
    rooms_types_available = ['Entire home/apt', 'Private room', 'Shared room']
    return rooms_types_available


def get_neighbourhood_groups():
    neighbourhood_groups_available = ['Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx']
    return neighbourhood_groups_available


def create_distribution_room_type_plot(data_frame):
    room_type_plot_graph = sns.catplot(x='room_type', col='neighbourhood_group',
                                       data=data_frame, kind='count',
                                       height=5, aspect=0.7)
    room_type_plot_graph.set_xticklabels(rotation=90)


def get_neighbourhood_group_room_types_average_price():
    room_types_average_price = pd.read_sql('''select neighbourhood_group,room_type,avg(price) 
    FROM ab_nyc_2019 where neighbourhood_group in (select neighbourhood_group from ab_nyc_2019 GROUP BY room_type) 
    GROUP BY neighbourhood_group,room_type''', con=mydb)
    return room_types_average_price


def create_plot_neighbourhood_group_room_types_average_price(rooms_types_available, room_types_average_price):
    plt.figure(figsize=(12, 8))
    sns.set_palette("Set1")
    for room in rooms_types_available:
        sns.lineplot(x='neighbourhood_group', y='avg(price)', data=room_types_average_price[room_types_average_price['room_type'] == room], label=room)
        plt.xlabel("Neighbourhood_group", size=13), plt.ylabel("Average price", size=13), plt.title("Neighbourhood_group "
                                                                                                "vs "
                                                                                                "Average Price vs "
                                                                                                "Room_type", size=15,
                                                                                                weight='bold')


def get_airbnb_neighbourhoods_in_neighbourhood_group_average_pricing():
    airbnb_neighbourhoods_in_neighbourhood_group_average_price = pd.read_sql('''select
    neighbourhood_group, neighbourhood, avg(price)
    FROM
    ab_nyc_2019
    where
    neighbourhood in (select neighbourhood from ab_nyc_2019 GROUP BY neighbourhood_group)
    GROUP
    BY
    neighbourhood, neighbourhood_group;con=mydb
    return airbnb_neighbourhoods_in_neighbourhood_group_average_price''', con=mydb)
    return airbnb_neighbourhoods_in_neighbourhood_group_average_price


def create_plot_airbnb_neighbourhoods_average_price(neighbourhood_groups_available,airbnb_neighbourhoods_in_neighbourhood_group_average_price):
    plt.figure(figsize=(12, 8))
    sns.set_palette("Set1")
    for neighbourhoods in neighbourhood_groups_available:
        sns.lineplot(x='neighbourhood', y='avg(price)',data=airbnb_neighbourhoods_in_neighbourhood_group_average_price[airbnb_neighbourhoods_in_neighbourhood_group_average_price['neighbourhood_group'] == neighbourhoods],label=neighbourhoods)
    plt.xlabel("Neighbourhood", size=13), plt.ylabel("Average price", size=13), plt.title(
        " Average Price vs Neighbourhood", size=15, weight='bold')


def get_five_locations_cheap_and_expensive(data):
    five_locations_cheap_and_expensive = airbnb_data.groupby(['neighbourhood', 'neighbourhood_group']).agg({'price': 'mean'}).reset_index()
    five_locations_cheap_and_expensive_neighbourhood_group = five_locations_cheap_and_expensive.groupby(["neighbourhood_group"]).apply(lambda x: x.sort_values(["price"], ascending=data)).reset_index(drop=True)
    top_five_neighbourhoods_price_list = five_locations_cheap_and_expensive_neighbourhood_group.groupby('neighbourhood_group').head(5)
    top_five_neighbourhoods_price_list = top_five_neighbourhoods_price_list.rename(columns={'price': 'avp'})
    return top_five_neighbourhoods_price_list


def create_plot_for_five_rooms_in_each_neighbourhood_group(neighbourhood_groups_available, top_five_neighbourhoods_price_list):
    for neighbourhood_group_location in neighbourhood_groups_available:
        ax = sns.relplot(x='neighbourhood', y='avp', col='neighbourhood_group',
                          data=top_five_neighbourhoods_price_list[top_five_neighbourhoods_price_list['neighbourhood_group'] == neighbourhood_group_location], height=5,
                          aspect=0.7)
        ax.set_xticklabels(rotation=90)


def get_density_check_of_room_pricing_among_neighbourhood_group():
    density_check_of_room_pricing_among_neighbourhood_group = airbnb_data[airbnb_data.price < 500]
    density_rooms_plot = sns.violinplot(data=density_check_of_room_pricing_among_neighbourhood_group, x='neighbourhood_group', y='price')
    density_rooms_plot.set_title('Density and distribution of prices for each neighbourhood_group')


def get_wordcloud_for_airbnb_cheap_locations_highlighted(room_price):
    plt.subplots(figsize=(25, 15))
    wordcloud = WordCloud(
        background_color='green',
        width=1800,
        height=1000).generate(" ".join(room_price.neighbourhood))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()


airbnb_data = get_ingested_data_from_csv()
create_distribution_room_type_plot(airbnb_data)
room_types_of_neighbourhood_group = room_types()
neighbourhood_group_room_types_average_price = get_neighbourhood_group_room_types_average_price()
create_plot_neighbourhood_group_room_types_average_price(room_types_of_neighbourhood_group, neighbourhood_group_room_types_average_price)
neighbourhoods_in_neighbourhood_group_average_price = get_airbnb_neighbourhoods_in_neighbourhood_group_average_pricing()
neighbourhood_groups = get_neighbourhood_groups()
create_plot_airbnb_neighbourhoods_average_price(neighbourhood_groups, neighbourhoods_in_neighbourhood_group_average_price)
neighbourhood_group_cheap_5_locations = get_five_locations_cheap_and_expensive('true')
create_plot_for_five_rooms_in_each_neighbourhood_group(neighbourhood_groups, neighbourhood_group_cheap_5_locations)
neighbourhood_group_expensive_5_locations = get_five_locations_cheap_and_expensive('false')
create_plot_for_five_rooms_in_each_neighbourhood_group(neighbourhood_groups, neighbourhood_group_expensive_5_locations)
get_density_check_of_room_pricing_among_neighbourhood_group()
get_wordcloud_for_airbnb_cheap_locations_highlighted(neighbourhood_group_cheap_5_locations)


