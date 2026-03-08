from fs_tools import read_file, list_files, search_in_file, write_file

print("AI Resume Assistant")
print("--------------------")

while True:

    user_input = input("\nUser: ").lower()

    if user_input == "exit":
        break


    # READ RESUMES
    elif "read" in user_input and "resume" in user_input:

        files = list_files("resumes")

        for file in files:
            path = "resumes/" + file["name"]

            data = read_file(path)

            if data["success"]:
                print("\nResume:", file["name"])
                print(data["content"][:200])


    # SEARCH KEYWORD
    elif "find" in user_input:

        keyword = user_input.split()[-1]

        files = list_files("resumes")

        for file in files:

            path = "resumes/" + file["name"]

            result = search_in_file(path, keyword)

            if result["success"] and result["matches"]:
                print("\nFound in:", file["name"])
                print(result["matches"])


    # CREATE SUMMARY
    elif "summary" in user_input:

        filename = user_input.split()[-1]

        path = "resumes/" + filename

        data = read_file(path)

        if data["success"]:

            text = data["content"]

            summary = text[:150] + "..."

            write_file("summaries/summary_" + filename, summary)

            print("Summary created!")

        else:
            print("File not found")


    else:
        print("Sorry, I didn't understand.")