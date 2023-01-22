from api.settings import MEDIA_URL


class ImageCommon:
    @staticmethod
    def get_image(image):
        if image:
            return '{}{}'.format(MEDIA_URL, image)
        return ''
