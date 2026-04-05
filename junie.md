# Junie Guideline: Seminar Slide Generator

This project is a tool for generating a structured, web-based presentation for the "Seminar 2026" course. It processes a
text-based curriculum plan and transforms it into a set of interactive HTML slides and a central index page.

## Project Overview

The generator is designed to create a consistent and responsive learning experience. It includes custom styling,
iconography, and command examples for every slide in the curriculum.

### Core Components

- **`generate_slides.py`**: The primary Python script that drives the generation process. It parses the curriculum plan,
  generates individual HTML files for each slide, and creates an `index.html` as the entry point.
- **`plan.txt`**: A structured text file containing the seminar curriculum, divided into Parts, Days, and Slides.
- **`slides/`**: A directory (automatically created) that stores the generated HTML slide files.
- **`index.html`**: The main landing page that provides an overview of the course and links to all slides.

## Usage Instructions

### Running the Generator

To generate or update the seminar slides, execute the following command from the project root:

```bash
python3 generate_slides.py
```

Upon successful execution, the script will:

1. Parse the curriculum defined in `plan.txt`.
2. Create or update the `slides/` directory.
3. Generate an HTML file for every slide found in the plan.
4. Update `index.html` with the latest course structure.

### Managing the Slides Directory

- **Auto-Generation**: The `slides/` directory is automatically managed by the script. You do not need to create it
  manually.
- **Cleanup**: If you modify the slide numbering in `plan.txt` and wish to remove old, orphaned slide files, you can
  safely delete the `slides/` directory before running the script again.
- **Asset Dependencies**: The generated HTML files are self-contained in terms of structure and logic, but they rely on
  external fonts (Inter, Prompt) and CDNs for icons (SVG-based).

### Editing the Curriculum

To change the content of the slides:

1. Edit `plan.txt` following the existing format:
    - `Part [Number]: [Title]`
    - `วันที่ [Number]: [Title]`
    - `Slide [Number]: [Content]`
2. Re-run `generate_slides.py`.
3. If you need to add specific commands or detailed info to a new slide, update the `slide_details` dictionary within
   `generate_slides.py` using the `"DayNumber_SlideNumber"` key format.

## Commit Guidelines

When making changes to this repository, please follow
the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. Use the following prefixes for
your commit messages:

- **`feat:`**: A new feature (e.g., feat: adding a new slide or a new component).
- **`fix:`**: A bug fix (e.g., fix: correcting a typo in a slide).
- **`chore:`**: Regular maintenance tasks (e.g., chore: updating dependencies or `.gitignore`).
- **`docs:`**: Documentation-only changes (e.g., docs: updating `junie.md`).
- **`refactor:`**: A code change that neither fixes a bug nor adds a feature (e.g. refactor: query optimize).
- **`style:`**: Changes that do not affect the meaning of the code (white-space, formatting, etc.) (e.g. style: adjust
  tab to read easier).
- **`test:`**: Adding missing tests or correcting existing tests(e.g. test: add test for a new component).
