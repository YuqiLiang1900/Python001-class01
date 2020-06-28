import requests
from bs4 import BeautifulSoup as bs
from requests.exceptions import RequestException
import pandas as pd


class MaoyanSpider():
    name = 'maoyan'
    allowed_domains = ['m.maoyan.com']
    original_url = ['https://m.maoyan.com/?showType=3#movie/classic']
    df = pd.DataFrame(columns=['电影名', '类别', '上映时间', '链接'])

    def get_one_page(self, film_number):
        """
        Return a list of responses depending on how many web pages we are going to scrape.
        But the number of web pages also depends on how many films we are going to sprape.
        """
        response_list = []

        for i in range(0, (film_number + 1 - 10), 10):

            url = 'https://m.maoyan.com/ajax/moreClassicList?sortId=1&showType=3&limit=10&offset={}\
                &optimus_uuid=1EAC78C0B6EF11EAAF59052F3C3ECF63F9B57BD35D90469CA9D64879E1D591F1&optimus_risk_level=71\
                    &optimus_code=10'.format(i)

            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
            header = dict()
            header['user-agent'] = user_agent
            header['Cookie'] = 'uuid_n_v=v1; uuid=CAF8C5B0B46111EA9736CB82F1E06989BD2F5A06FB0B43F0855DDA3467D891A1; _lxsdk_cuid=172db21146cc8-0d1b5d8ce6dcc2-3469780f-13c680-172db21146cc8; _lxsdk=CAF8C5B0B46111EA9736CB82F1E06989BD2F5A06FB0B43F0855DDA3467D891A1; mojo-uuid=b887dfc2b7a9b96482df85ac2335dcd1; _csrf=1baff4f8d86793bcc5c1f5439b85aa944561ce8687c59fe38d13e466dcc107e9; mojo-session-id={"id":"8202c12aeb7ba4d862cb54cf0ba1c87c","time":1593091883810}; mojo-trace-id=1; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592814277,1592896312,1593091884; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593091884; __mta=42776346.1592814277813.1592896607842.1593091884382.8; _lxsdk_s=172ebad04ee-6b-83-4da%7C%7C2'
            response = requests.get(url, headers=header)

            try:
                if response.status_code == 200:
                    response_list.append(response)
            except RequestException:
                return print("Error while accessing the web page.")

        return response_list

    def sparse_one_page(self, response):
        
        bs_info = bs(response.text, 'html.parser')

        title_list = []
        genres_list = []
        release_date_list = []
        link_list = []

        for tags in bs_info.find_all('div', attrs={'class': 'movie-info'}):

            title = tags.find(class_='title line-ellipsis').text
            genres = tags.find(class_='actors line-ellipsis').text
            release_date = tags.find(class_='show-info line-ellipsis')

            if release_date is not None:
                release_date = tags.find(class_='show-info line-ellipsis').text[:10]

            print('Title:', title)
            print('Genres: ', genres)
            print('Release date: ', release_date)

            title_list.append(title)
            genres_list.append(genres)
            release_date_list.append(release_date)

        for tags in bs_info.find_all('a'):
            # print('tags:', tags)
            # Get the link of the movie
            link = '{}{}'.format(self.allowed_domains[0], tags.get('href'))
            print('Link: {}'.format(link))
            link_list.append(link)

        info_dict = dict()
        info_dict['title_list'] = title_list
        info_dict['genres_list'] = genres_list
        info_dict['release_date_list'] = release_date_list
        info_dict['link_list'] = link_list

        return info_dict

    def load_to_df(self, **df_entries_tuple):
        
        temp_df = pd.DataFrame(columns=['电影名', '类别', '上映时间', '链接'])
        temp_df['电影名'] = df_entries_tuple['title_list']
        temp_df['类别'] = df_entries_tuple['genres_list']
        temp_df['上映时间'] = df_entries_tuple['release_date_list']

        temp_df['链接'] = df_entries_tuple['link_list']

        def concancate_dfs(temp_df):
            concat_df = pd.concat([self.df, temp_df])
            return concat_df

        self.df = concancate_dfs(temp_df)
        return self.df

    def save_to_csv(self):
        self.df = self.df.reset_index(drop=True)
        self.df.to_csv('homework1_{}.csv'.format(self.name))
        print('Successfully saved the dataframe to a csv called {}.csv'.format(self.name))


if __name__ == '__main__':
    maoyanspider = MaoyanSpider()
    response_list = maoyanspider.get_one_page(10)
    for response in response_list:
        info_dict = maoyanspider.sparse_one_page(response)
        df = maoyanspider.load_to_df(title_list=info_dict['title_list'],
                                     genres_list=info_dict['genres_list'],
                                     release_date_list=info_dict['release_date_list'],
                                     link_list=info_dict['link_list']
                                     )
    maoyanspider.save_to_csv()
