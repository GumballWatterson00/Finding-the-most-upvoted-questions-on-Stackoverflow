import sys
import requests
import html

question_number = int(sys.argv[1])
question_label = sys.argv[2]

session = requests.session()

url = 'https://api.stackexchange.com/2.2/questions'


class OverFlow(Exception):
    pass


def pages(number):
    page_items_counting = []
    for page in range(number // 100):
        page_items_counting.append(100)
    if number % 100 != 0:
        page_items_counting.append(number % 100)
    return page_items_counting


def top_questions(number, label):
    pagesizes = pages(number)
    try:
        top_ques = []
        for page, pagesize in enumerate(pagesizes, 1):
            parameters = {"page": page,
                          "pagesize": pagesize,
                          "order": "desc",
                          "sort": "votes",
                          "tagged": label,
                          "site": "stackoverflow"}
            response = session.get(url, params=parameters).json()
            for item in response["items"]:
                title = html.unescape(item["title"])
                question_id = item["question_id"]
                top_ques.append((title, question_id))
        return top_ques
    except Exception:
        raise OverFlow("Too many requests from this IP")


def top_answer(question_id):
    link = f'{url}/{question_id}/answers'
    parameters = {"pagesize": 1,
                  "order": "desc",
                  "sort": "votes",
                  "site": "stackoverflow"}
    try:
        response = session.get(link, params=parameters).json()
        answer = response["items"][0]['answer_id']
        return answer
    except Exception:
        raise OverFlow("Too many requests from this IP")


def main():
    print(f'Top {question_number} questions with tag {question_label}')
    if question_number >= 300:
        print("Too many requests from this IP")
        return

    questions = top_questions(question_number, question_label)
    index = 0
    for title, question_id in questions:
        answer_id = top_answer(question_id)
        link_to_answer = f'https://stackoverflow.com/a/{answer_id}'
        index += 1
        print(f"\n\n{index}\n{title}\nAnswer: {link_to_answer}")


if __name__ == "__main__":
    main()
