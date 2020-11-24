

def exportfits_wrapper(output_directory, imagename, extensions=["image"]):

    for ext in extensions:

        imagename = "{}/{}.{}".format(
            output_directory,
            imagename,
            ext
        )
        if os.path.dir(imagename):
            exportfits(
                imagename="{}/{}.{}".format(
                    output_directory,
                    imagename,
                    ext
                ),
                fitsimage="{}/{}.{}.fits".format(
                    output_directory,
                    imagename,
                    ext
                ),
                overwrite=True
            )
        else:
            raise IOError(
                "The directory {} does not exist".format(imagename)
            )
