import os
import shutil


class FileManager:
    def __init__(self, base_folder="images"):
        self.base_folder = base_folder
        if not os.path.exists(base_folder):
            os.makedirs(self.base_folder)

    async def save_image(self, id, image_name, tag):

        if not os.path.exists(f"images\\{id}"):
            os.mkdir(f"images\\{id}")

        if not os.path.exists(f"images\\{id}\\{tag}"):
            os.mkdir(f"images\\{id}\\{tag}")

        src = str(os.path.join(image_name))
        dest = str(os.path.join(self.base_folder, id, tag))

        os.makedirs(os.path.dirname(dest), exist_ok=True)
        dest = str(os.path.join(self.base_folder, id, tag, image_name))

        shutil.copy(src, dest)
        os.remove(src)
