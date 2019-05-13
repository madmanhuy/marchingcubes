import os

import click

from marchingcubes.algorithm import march
from marchingcubes.utilities import read_dicom_image, process_image


@click.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True), required=True)
@click.argument('resolution', type=click.INT)
def cli(path, resolution):
    image_list = [image for image in os.listdir(path) if image.endswith(('.dcm', '.png'))]
    click.echo("Found {} images in {}" .format(len(image_list), path))

    for i, image in enumerate(image_list):

        if image.endswith('.dcm'):
            png_path = read_dicom_image(os.path.join(path, image))
            process_image(png_path)
        else:
            process_image(os.path.join(path, image))

    vertices, faces = march(path, resolution)
    click.echo("Total number of vertices: {}" .format(len(vertices)))
    click.echo("Total number of faces: {}" .format(len(faces)))
    click.echo("Writing to output.obj")

    with open('output.obj', 'w') as obj_file:
        for vertex in vertices:
            obj_file.write("v {} {} {}\n".format(vertex[0], vertex[1], vertex[2]))
        for face in faces:
            obj_file.write("f {} {} {}\n".format(face[0], face[1], face[2]))

    click.echo("Finished writing OBJ file: {}/output.obj" .format(os.getcwd()))
