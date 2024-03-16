from youtube_search import YoutubeSearch

def search_album(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    return results

def print_results(results):
    if results:
        print("1. ", results[0]['title'])  # Print only the first result
    else:
        print("No results found for the query.")

if __name__ == "__main__":
    query = input("Enter album name and artist name: ")
    results = search_album(query)
    print_results(results)
 