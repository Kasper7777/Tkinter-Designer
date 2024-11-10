import tkdesigner.figma.endpoints as endpoints
from tkdesigner.figma.frame import Frame

from tkdesigner.template import TEMPLATE

from pathlib import Path

class Designer:
    def __init__(self, token, file_key, output_path: Path):
        self.output_path = output_path
        self.figma_file = endpoints.Files(token, file_key)
        self.file_data = self.figma_file.get_file()
        self.frameCounter = 0

    def to_code(self) -> str:
        """Return main code."""
        frames = []
        try:
            for f in self.file_data["document"]["children"][0]["children"]:
                print("Accessing frame data:", f)  # Debug output for frame data

                try:
                    frame = Frame(f, self.figma_file, self.output_path, self.frameCounter)
                    if frame.elements is None:
                        raise Exception(f"Frame {self.frameCounter} has no elements.")
                    frames.append(frame.to_code(TEMPLATE))
                    self.frameCounter += 1
                except Exception as e:
                    print(f"Error processing frame {self.frameCounter}: {e}")
                    continue  # Skip this frame if there's an error

            if not frames:
                raise Exception("No frames found or all frames are empty.")
            return frames
        except KeyError:
            raise Exception("The file structure is unexpected. 'document' or 'children' keys are missing.")

    def design(self):
        """Write code and assets to the specified directories."""
        code = self.to_code()
        if not code:
            raise Exception("No code generated, possibly due to empty frames.")

        for index, code_str in enumerate(code):
            filename = "gui.py" if index == 0 else f"gui{index}.py"
            self.output_path.joinpath(filename).write_text(code_str, encoding='UTF-8')

