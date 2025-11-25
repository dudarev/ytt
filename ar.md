File inspired by [The append-and-review note idea by Andrej Karpathy](https://karpathy.bearblog.dev/the-append-and-review-note/)

Consider adding explicit link to the YouTube video from which the transcript is extracted. 

Create a separate library to get a video title and description for YouTube from parsing the page. it can be heavily AI coded we can get several pages as an example and and devise a strategy to extract description and titlec:qo separate description from the transcript or h2-level sections (Description, Transcript)

Have config to include the title and the description

Automatically copy
    Potentially a setting to disable this option

```
pip install pyperclip
import pyperclip
pyperclip.copy("Text to copy")
```

Use the content of the clipboard as input if no parameters are specified, assuming a YouTube link is copied to the clipboard.
If no parameters are specified, use the clipboard content (assumed to be a YouTube link) as input; this enables idempotent, reusable operations when the same URL is used repeatedly.

Provide a configurable prefix (prompt) that can be added to the output. This is useful for workflows where transcripts are frequently summarized, allowing a custom prompt to be prepended automatically.

Set up CI

Write the most important tests

Ensure supported URL formats are consistent between README and code.

Introduce (architecture) decision records - ADR 0002 about ADRs

Introduce some rules for AI assistants (see "AI Assistant Instruction Conventions" in Dev)

Potentially split into packages

Regularly clean unnecessary comments

Return also the title of the video, it's description and the link to it

In the long run, we want to transcribe video if transcript is not available using local whisper or something like that.

Currently, we can output without the transcript the title and description and a message that transcript is not available.
Example video without a transcript: https://www.youtube.com/watch?v=v52PlPf4KUI
