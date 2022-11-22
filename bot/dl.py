import sys
from skillshare import download_course_by_url


def main():
    course_url = sys.argv[1]
    download_course_by_url(url=course_url)


if __name__ == "__main__":
    main()
