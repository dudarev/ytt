This document tracks ideas and tasks for improving the `ytt` tool. It's inspired by Andrej Karpathy's [append-and-review note-taking method](https://karpathy.bearblog.dev/the-append-and-review-note/).

- It may be useful to have a list of all the possible settings available in README and also in the help for the config command.

### High-Priority Tasks
- **Handle Videos Without Transcripts**: For videos lacking a transcript (e.g., [https://www.youtube.com/watch?v=v52PlPf4KUI](https://www.youtube.com/watch?v=v52PlPf4KUI)), output the title, description, and a message indicating the transcript is unavailable.
- **CI/CD**: Set up a continuous integration pipeline to automate testing and linting.
- **Write Key Tests**: Expand the test suite to cover critical user paths and edge cases.

### Medium-Priority Tasks
- **Configurable Prefix**: Allow users to configure a prefix (e.g., a summarization prompt) to be automatically added to the output.
- **URL Format Consistency**: Ensure that the URL formats supported by the tool are consistent between the `README.md` and the implementation.
- **Regularly Clean Code**: Periodically remove unnecessary comments and refactor for clarity.

### Long-Term Goals
- **Local Transcription**: In the future, integrate a local transcription service (like Whisper) to handle videos that do not have a built-in transcript.

### Completed Tasks
- Output video title, description, and URL
- Separate transcript, description, and title with Markdown headings
- Automatically copy output to clipboard
- Configure output sections (title, description, etc.)
- Use a structured, package-based architecture
- Introduce ADRs and AI assistant guidelines
- **Clipboard as Input**: If no URL is provided, use the clipboard's content as the input URL. This allows for faster, idempotent workflows when working with the same link repeatedly.
