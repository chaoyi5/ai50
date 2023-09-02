import csv
import sys 
# https://blog.louie.lu/2017/07/26/%E4%BD%A0%E6%89%80%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84-python-%E6%A8%99%E6%BA%96%E5%87%BD%E5%BC%8F%E5%BA%AB%E7%94%A8%E6%B3%95-01-sys/

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    # open(f"{...} 那個f是做什麼用的
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # 一行一行讀??
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set() # 創建一個無序不重複元素集
            }
            # ???
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])


    # Load movies：用 person_id 找對應的 movie_id
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars：用 movie_id 找對應的 movie_name
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass # 不做任何事情


def main():
    if len(sys.argv) > 2: # 為什為什麼是>2 ，是要用來判斷什麼呢?
        sys.exit("Usage: python degrees.py [directory]")
        # 上面的寫法和sys.exit()的效果有什麼區別呢?
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    # directory = small or large
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    # 如果 path = [('movie_id1','person_id1'),('movie_id2','person_id2')]，那 len(path) = 2

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            # people[path[i][1]]["name"]這是指...
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    start = Node(state=source, parent=None, action=None)
    # frontier是指那些people的集合嗎
    frontier = QueueFrontier()
    frontier.add(start)

    explored = set()
    # 甚麼事件為true?，這段不太明白
    while True:
        if frontier.empty():
            return None

        node = frontier.remove()

        if node.state == target:
            rt = []

            while node.parent is not None:
                rt.append((node.action, node.state))
                node = node.parent

            rt.reverse()
            return rt

        explored.add(node.state)


        # find neighbours
        neighbours = neighbors_for_person(node.state)

        # add neighbours to frontier
        for action, state in neighbours:
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                if child.state == target:
                    rt = []

                    while child.parent is not None:
                        # append：將元素加在串列最後面
                        rt.append((child.action, child.state))
                        child = child.parent

                    rt.reverse()
                    return rt
                # add：给集合添加元素
                frontier.add(child)

# 找 name 對應的 person_id
def person_id_for_name(name):
    # 網路電影資料庫（IMDB，Internet Movie Database)
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    # 在姓名清單中找名字，找不到就輸出none
    person_ids = list(names.get(name.lower(), set())) # set() 必要??
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        # 為什麼不是直接 person_ids
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    # 用 person_id 和 movies 來找對應的 movie_ids 
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    # 再用 movie_ids 來找對應的 stars
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

    """
    if __name__=='__main__': 這段程式碼在程式被引用時不會執行，
    只要自己在執行的時候會呼叫，這樣就可以避免呼叫別的檔案的函式時又被執行到。
    https://ithelp.ithome.com.tw/articles/10277352
    """
    
if __name__ == "__main__":
    main()
