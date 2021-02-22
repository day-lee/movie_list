import requests
API_KEY = "814409d5db6882438b9cd579f376406c"
#title = "Spirited away"#form.title.data


# parameters = {
#     "api_key": API_KEY,
#     "query": title,
# }
#
#
# response = requests.get("https://api.themoviedb.org/3/search/movie", params=parameters)
# response.raise_for_status()
#
# data = response.json()
# result = data['results']
# print(data)
# print(result)
#
# for movie in result:
#     print('--------')
#     print(movie['title'])
#     print(movie['release_date'])
#     print(movie['overview'])
#     print(movie['id'])
#     print('--------')

#-------------
movie_id= '698296'
parameters = {
    "api_key": API_KEY
}
detail_response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}", params=parameters)
detail_response.raise_for_status()

detail_data = detail_response.json()
title = detail_data['title']
year = detail_data['release_date']
img_url = detail_data['poster_path']
description = detail_data['overview']

