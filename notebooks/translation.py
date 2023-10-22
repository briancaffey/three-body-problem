import json

def translate_chapter(llm, book_path, chapter_number):
    """
    Using an LLM, this function adds text transformations to JSON files

        - The JSON file corresponds to the chapter of a book
        - The keys written to the JSON file are for the following transformations:
            - Chinese to English translation
            - Chinese summarization (1 or 2 sentences)
            - Translation of the Chinese summary into English
    """

    # system prompts
    cn_en_translation_system_prompt = "你是一名翻译。请将每条消息从中文翻译成英文。"
    cn_summary_system_prompt = "用中文概括下列文字"

    JSON_FILE = f"../data/books/{book_path}/chapters/{chapter_number}.json"

    # open the file
    with open(JSON_FILE, "r") as f:

        chapter = json.loads(f.read())
        cn_en_translations = []
        cn_summaries = []
        en_summaries = []

        # the paragraphs key is a list of strings. Each string is text of a paragraph
        for paragraph in chapter["paragraphs"]:

            print()
            print("original text")
            print()
            print(paragraph)

            # translate cn to en
            print()
            print("translate from Chinese to English")
            print()
            translated_paragraph = llm.inference(
                cn_en_translation_system_prompt,
                paragraph,
            )
            print(translated_paragraph)
            cn_en_translations.append(translated_paragraph)

            # cn_summary
            print()
            print("summarize using Chinese")
            print()
            cn_summary = llm.inference(
                cn_summary_system_prompt,
                paragraph,
            )
            print(cn_summary)
            cn_summaries.append(cn_summary)

            # en_summary
            print()
            print("Translate Chinese summary to English")
            print()
            en_summary = llm.inference(
                cn_en_translation_system_prompt,
                cn_summary,
            )
            print(en_summary)
            en_summaries.append(en_summary)

        chapter[f"en_translation_{llm.short_name}"] = cn_en_translations
        chapter[f"cn_summaries_{llm.short_name}"] = cn_summaries
        chapter[f"en_summaries_{llm.short_name}"] = en_summaries

    with open(f"../data/books/{book_path}/chapters/{chapter_number}.json", "w") as f:
        json.dump(chapter, f, ensure_ascii=False)

    print(f"translated {len(cn_en_translations)}.")