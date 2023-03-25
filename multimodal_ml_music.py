"""
Code adapted from https://github.com/ybayle/awesome-deep-learning-music (written by Yann Bayle)
======================
Parse multimodal_ml_music.bib to create a simple and readable README.md table.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import bibtexparser
from bibtexparser.bwriter import BibTexWriter


def write_bib(bib_database, filen="multimodal_ml_music.bib"):
    """
    Write the items stored in bib_database into filen
    """
    writer = BibTexWriter()
    writer.indent = "  "
    writer.order_entries_by = ("year", "author")
    with open(filen, "w", encoding="utf-8") as bibfile:
        bibfile.write(writer.write(bib_database))


def read_bib(filen="multimodal_ml_music.bib"):
    """
    Parse a bib file and load it into memory in a python format
    """
    with open(filen, "r", encoding="utf-8") as bibtex_file:
        bibtex_str = bibtex_file.read()
    bib_database = bibtexparser.loads(bibtex_str)
    return bib_database


def load_bib(filen="multimodal_ml_musi.bib"):
    """
    Load and return the items stored in filen
    """
    bib = read_bib(filen)
    write_bib(bib, filen)
    bib = read_bib(filen)
    return bib.entries


def articles_per_year(bib):
    """
    Display the number of articles published per year
    input: file name storing articles details
    """
    years = []
    for entry in bib:
        year = int(entry["year"])
        years.append(year)

    plt.xlabel("Year")
    plt.ylabel("Number of articles on Multimodal ML for Music")
    year_bins = np.arange(min(years), max(years) + 2.0, 1.0)
    plt.hist(years, bins=year_bins, color="#401153", align="left")
    axe = plt.gca()
    axe.spines["right"].set_color("none")
    axe.spines["top"].set_color("none")
    axe.xaxis.set_ticks_position("bottom")
    axe.yaxis.set_ticks_position("left")
    fig_fn = "fig/articles_per_year.png"
    plt.savefig(fig_fn, dpi=200)
    print("Fig. with number of articles per year saved in", fig_fn)


def get_reproducibility(bib):
    """
    Generate insights on reproducibility
    """
    cpt = 0
    for entry in bib:
        if "code" in entry:
            if entry["code"][:2] != "No":
                cpt += 1
    print(str(cpt) + " articles provide their source code.")

    return cpt


def get_nb_articles(bib):
    """
    Count the number of articles in the database
    """
    print("There are", len(bib), "articles referenced.")
    return len(bib)


def get_authors(bib):
    """
    Print in authors.md the alphabetical list of authors
    """
    authors = []
    for entry in bib:
        for author in entry["author"].split(" and "):
            authors.append(author)
    authors = sorted(set(authors))
    nb_authors = len(authors)
    print("There are", nb_authors, "researchers working on multimodal_ml_music.")

    authors_fn = "authors.md"
    with open(authors_fn, "w", encoding="utf-8") as filep:
        filep.write("# List of authors\n\n")
        for author in authors:
            filep.write("- " + author + "\n")
    print("List of authors written in", authors_fn)

    return nb_authors


def generate_list_articles(bib):
    """
    From the bib file generates a ReadMe-styled table like:
    | [Name of the article](Link to the .pdf) | Code's link if available |
    """
    articles = ""
    for entry in bib:
        if "title" in entry:
            if "year" in entry:
                articles += "| " + entry["year"] + " "
            else:
                print("ERROR: Missing year for ", entry)
                sys.exit()
            if "link" in entry:
                articles += "| [" + entry["title"] + "](" + entry["link"] + ") | "
            else:
                articles += "| " + entry["title"] + " | "
            if "code" in entry:
                if "No" in entry["code"]:
                    articles += "No "
                else:
                    if "github" in entry["code"]:
                        articles += "[GitHub"
                    else:
                        articles += "[Website"
                    articles += "](" + entry["code"] + ") "
            if "type" in entry:
                articles += "| " + entry["type"]
            else:
                articles += "| Other"
            articles += "|\n"
        else:
            print("ERROR: Missing title for ", entry)
            sys.exit()

    # articles += "|------|-------------------------------|------|\n| Year |  Paper Title | Code |"
    sorted_articles = ""
    for line in sorted(articles.split("\n"), key=lambda line: line.split("|")[0])[::-1]:
        sorted_articles += line + "\n"
    return sorted_articles


def generate_summary_table(bib):
    """
    Parse multimodal_ml_music.bib to create a simple and readable ReadMe.md table.
    """
    nb_articles = get_nb_articles(bib)
    nb_repro = get_reproducibility(bib)
    percent_repro = str(int(nb_repro * 100.0 / nb_articles))
    nb_articles = str(nb_articles)
    nb_repro = str(nb_repro)
    nb_authors = str(get_authors(bib) - 1)
    nb_tasks = str(get_field(bib, "task"))
    nb_datasets = str(get_field(bib, "dataset"))
    articles = generate_list_articles(bib)

    audio_text_articles = ""
    audio_image_articles = ""
    audio_video_articles = ""
    audio_eeg_articles = ""
    audio_user_articles = ""
    other_articles = ""
    for article in articles.splitlines():
        if article != "":
            if "Audio-Text" in article.split("|")[-2]:
                audio_text_articles += (" | ").join(article.split("|")[:-2]) + "\n"
            elif "Audio-Image" in article.split("|")[-2]:
                audio_image_articles += (" | ").join(article.split("|")[:-2]) + "\n"
            elif "Audio-Video" in article.split("|")[-2]:
                audio_video_articles += (" | ").join(article.split("|")[:-2]) + "\n"
            elif "Audio-EEG" in article.split("|")[-2]:
                audio_eeg_articles += (" | ").join(article.split("|")[:-2]) + "\n"
            elif "Audio-User" in article.split("|")[-2]:
                audio_user_articles += (" | ").join(article.split("|")[:-2]) + "\n"
            else:
                other_articles += (" | ").join(article.split("|")[:-2]) + "\n"

    readme_fn = "README.md"
    readme = ""
    pasted_at_articles = False
    pasted_ai_articles = False
    pasted_av_articles = False
    pasted_ae_articles = False
    pasted_au_articles = False
    pasted_other_articles = False
    with open(readme_fn, "r", encoding="utf-8") as filep:
        for line in filep:
            # if "| " in line[:2] and line[2] != " ":
            if not pasted_at_articles and line == "#### Audio-Text\n":
                readme += "#### Audio-Text\n"
                readme += "| Year |  Paper Title | Code |\n|------|-------------------------------|------|\n"
                readme += audio_text_articles
                pasted_at_articles = True
            elif not pasted_ai_articles and line == "#### Audio-Image\n":
                readme += "#### Audio-Image\n"
                readme += "| Year |  Paper Title | Code |\n|------|-------------------------------|------|\n"
                readme += audio_image_articles
                pasted_ai_articles = True
            elif not pasted_av_articles and line == "#### Audio-Video\n":
                readme += "#### Audio-Video\n"
                readme += "| Year |  Paper Title | Code |\n|------|-------------------------------|------|\n"
                readme += audio_video_articles
                pasted_av_articles = True
            elif not pasted_au_articles and line == "#### Audio-User\n":
                readme += "#### Audio-User\n"
                readme += "| Year |  Paper Title | Code |\n|------|-------------------------------|------|\n"
                readme += audio_user_articles
                pasted_au_articles = True

            # others
            if not pasted_other_articles and line == "#### Other\n":
                readme += "#### Other\n"
                readme += "| Year |  Paper Title | Code |\n|------|-------------------------------|------|\n"
                readme += other_articles
                pasted_other_articles = True
            elif "papers referenced" in line:
                readme += "- " + nb_articles + " papers referenced. "
                readme += "See the details in [multimodal_ml_music.bib](multimodal_ml_music.bib).\n"
            elif "other researchers" in line:
                readme += "- If you are applying multimodal ML to music, there are ["
                readme += nb_authors + " other researchers](authors.md) "
                readme += "in your field.\n"
            elif "tasks investigated" in line:
                readme += "- " + nb_tasks + " tasks investigated. "
                readme += "See the list of [tasks](tasks.md).\n"
            elif "datasets used" in line:
                readme += "- " + nb_datasets + " datasets used. "
                readme += "See the list of [datasets](datasets.md).\n"
            elif "- Only" in line:
                readme += "- Only " + nb_repro + " articles (" + percent_repro
                readme += "%) provide their source code.\n"
            else:
                if (
                    "|  2" not in line
                    and "#### Audio-Text" not in line
                    and "#### Audio-Video" not in line
                    and "#### Audio-Image" not in line
                    and "#### Audio-User" not in line
                    and "#### Other" not in line
                    and "| Year |  Paper Title | Code |" not in line
                    and "|------|-------------------------------|------|" not in line
                ):
                    readme += line
    with open(readme_fn, "w", encoding="utf-8") as filep:
        filep.write(readme)
    print("New ReadMe generated")


def validate_field(field_name):
    """
    Assert the validity of the field's name
    """
    fields = [
        "task",
        "dataset",
        "author",
        "link",
        "title",
        "year",
        "journal",
        "code",
        "ENTRYTYPE",
    ]
    error_str = "Invalid field provided: " + field_name + ". "
    error_str += "Valid fields: " + "[%s]" % ", ".join(map(str, fields))
    assert field_name in fields, error_str


def make_autopct(values):
    """Wrapper for the custom values to display in the pie chart slices"""

    def my_autopct(pct):
        """Define custom value to print in pie chart"""
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return "{p:.1f}%  ({v:d})".format(p=pct, v=val)

    return my_autopct


def pie_chart(items, field_name, max_nb_slice=8):
    """
    Display a pie_chart from the items given in input
    """
    # plt.figure(figsize=(14, 10))
    sizes = []
    labels = sorted(set(items))
    for label in labels:
        sizes.append(items.count(label))

    labels = np.array(labels)
    sizes = np.array(sizes)
    if len(sizes) > max_nb_slice:
        new_labels = []
        new_sizes = []
        for _ in range(0, max_nb_slice):
            index = np.where(sizes == max(sizes))[0]
            if len(index) == len(labels):
                break
            new_labels.append(labels[index][0])
            new_sizes.append(sizes[index][0])
            labels = np.delete(labels, index)
            sizes = np.delete(sizes, index)
        new_labels.append(str(len(labels)) + " others")
        new_sizes.append(sum(sizes))
        labels = np.array(new_labels)
        sizes = np.array(new_sizes)

    colors = [
        "gold",
        "yellowgreen",
        "lightcoral",
        "lightskyblue",
        "red",
        "green",
        "bisque",
        "lightgrey",
        "#555555",
    ]

    tmp_labels = []
    for label in labels:
        if "[" in label:
            label = label[1:].split("]")[0]
        tmp_labels.append(label)
    labels = np.array(tmp_labels)

    # h = plt.pie(sizes, labels=labels, colors=colors, shadow=False,
    plt.pie(
        sizes,
        labels=labels,
        colors=colors,
        shadow=False,
        startangle=90,
        autopct=make_autopct(sizes),
    )

    # Display the legend
    # leg = plt.legend(h[0], labels, bbox_to_anchor=(0.08, 0.4))
    # leg.draw_frame(False)
    plt.axis("equal")
    fig_fn = "fig/pie_chart_" + field_name + ".png"
    plt.savefig(fig_fn, dpi=200)
    plt.close()
    print("Fig. with number of articles per year saved in", fig_fn)


def get_field(bib, field_name):
    """
    Generate insights on the field_name in the bib file
    """
    validate_field(field_name)
    nb_article_missing = 0
    fields = []
    for entry in bib:
        if field_name in entry:
            cur_fields = entry[field_name].split(" & ")
            for field in cur_fields:
                fields.append(field)
        else:
            nb_article_missing += 1
    print(
        str(nb_article_missing) + " entries are missing the " + field_name + " field."
    )
    nb_fields = len(set(fields))
    print(str(nb_fields) + " unique " + field_name + ".")

    field_fn = field_name + "s.md"
    with open(field_fn, "w", encoding="utf-8") as filep:
        filep.write("# List of " + field_name + "s\n\n")
        for field in sorted(set(fields)):
            filep.write("- " + field + "\n")
    print("List of " + field_name + "s written in", field_fn)

    if field_name == "task":
        pie_chart(fields, field_name)

    return nb_fields


def create_table(bib, outfilen="multimodal_ml_music.tsv"):
    """
    Generate human-readable table in .tsv form.
    """

    print("Generating the human-readable table as .tsv")
    # Gather all existing field in bib
    fields = []
    for entry in bib:
        for key in entry:
            fields.append(key)

    print("Available fields:")
    print(set(fields))
    fields = [
        "year",
        "ENTRYTYPE",
        "title",
        "author",
        "link",
        "code",
        "task",
        "reproducible",
        "dataset",
        "framework",
        "architecture",
        "dropout",
        "batch",
        "epochs",
        "dataaugmentation",
        "input",
        "dimension",
        "activation",
        "loss",
        "learningrate",
        "optimizer",
        "gpu",
    ]
    print("Fields taken in order (in this order):")
    print(fields)

    separator = "\t"
    str2write = ""
    for field in fields:
        str2write += field.title() + separator
    str2write += "\n"
    for entry in bib:
        for field in fields:
            if field in entry:
                str2write += entry[field]
            str2write += separator
        str2write += "\n"
    with open(outfilen, "w", encoding="UTF-8") as filep:
        filep.write(str2write)


def where_published(bib):
    """Display insights on where the articles have been published"""
    journals = []
    conf = []
    for entry in bib:
        if "article" in entry["ENTRYTYPE"]:
            journals.append(entry["journal"])
        elif "inproceedings" in entry["ENTRYTYPE"]:
            conf.append(entry["booktitle"])
    journals = sorted(set(journals))
    conf = sorted(set(conf))

    with open("publication_type.md", "w") as filep:
        filep.write("# List of publications type\n\n### Journals:\n\n- ")
        filep.write("\n- ".join(journals))
        filep.write("\n\n### Conferences:\n\n- ")
        filep.write("\n- ".join(conf))
        filep.write("\n")


def main(filen="multimodal_ml_music.bib"):
    """
    Main entry point
    input: file name storing articles details
    """
    bib = load_bib(filen)
    generate_summary_table(bib)
    articles_per_year(bib)
    create_table(bib)
    where_published(bib)


if __name__ == "__main__":
    main("multimodal_ml_music.bib")
