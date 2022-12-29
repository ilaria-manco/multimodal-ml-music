# How to contribute to MML4Music
You can contribute by adding papers, datasets or other resources.

To do so:
1. Fork the repo
2. Add a new entry (see instructions below for more details on how to do this depending on the type of entry)
3. (Install `numpy`, `matplotlib`, `bibtexparser`, if not already installed)
4. Run the [multimodal_ml_music.py](./multimodal_ml_music.py) Python script
5. Submit a pull request

If you spot an issue or have trouble adding a new entry following the steps above, feel free to open an issue instead.

## Adding papers
To add a new paper, edit the [Bibtex file](multimodal_ml_music.bib) and add a new entry in the same format:

```
@newentrytype{EntryKey,
  title = {},
  author = {},
  year = {},
  dataset = {},
  code = {},
  link = {},
  task = {}
}
```

## Adding datasets
To add a new dataset, simply edit the [README.md](README.md) file and add a new row to the dataset table following the same format and adding the required information in each column.

## Adding other resources
Other resources can include: models, open-source projects, workshops, learning resources and similar. To add a new entry of this kind, edit the relevant section of the [README.md](README.md) file and add a new item to the list.
