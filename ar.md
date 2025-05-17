File inspired by [The append-and-review note idea by Andrej Karpathy](https://karpathy.bearblog.dev/the-append-and-review-note/)

Output the title and the link in the beginning

Output YouTube provided description in the beginning

Use --- to separate description from the transcript or h2-level sections (Description, Transcript)

Have config to include the title and the description

Automatically copy
    Potentially a setting to disable this option

```
pip install pyperclip
import pyperclip
pyperclip.copy("Text to copy")
```

Set up CI

Write the most important tests

Ensure supported URL formats are consistent between README and code.

Introduce (architecture) decision records - ADR 0002 about ADRs

Introduce some rules for AI assistants (see "AI Assistant Instruction Conventions" in Dev)

Potentially split into packages

Regularly clean unnecessary comments

Return also the title of the video, it's description and the link to it