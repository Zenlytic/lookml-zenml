import os
import json

import click
import lkml
import yaml

from .lookml_project import LookMLProject


def _convert_logic(path: str, directory: str, out_directory: str, convert_type: str):
    abs_path = os.path.abspath(path)
    with open(abs_path, "r") as file:
        if convert_type == "dashboard":
            lkml_result = yaml.safe_load(file)
        else:
            lkml_result = lkml.load(file)

    if directory:
        object_names = []
        to_loop = [lkml_result] if convert_type == "model" else lkml_result
        for o in lkml_result:
            if convert_type == "model":
                o["name"] = path.split(".")[-3].split("/")[-1]
            key = "name" if convert_type != "dashboard" else "dashboard"
            object_names.append(o[key])
        project = LookMLProject(in_directory=directory)
        lookml_project = project.load(project.in_directory)
        models, views, dashboards = project.convert_project(lookml_project)
        if convert_type == "dashboard":
            objects = dashboards
        elif convert_type == "model":
            objects = models
        elif convert_type == "view":
            objects = views
        else:
            raise ValueError(f"Unknown convert_type {convert_type}")
        result_objects = [o for o in objects if o["name"] in object_names]
    else:
        if convert_type == "dashboard":
            raise ValueError("Dashboards need context from the --directory argument to successfully convert")
        else:
            result_objects = []
            to_loop = lkml_result["views"] if convert_type == "view" else [lkml_result]
            for o in to_loop:
                if convert_type == "model":
                    o["name"] = path.split(".")[-3].split("/")[-1]
                    model = LookMLProject().convert_model(o)
                    result_objects.append(model)
                elif convert_type == "view":
                    result_objects.append(LookMLProject().convert_view(o, model_name="TODO add model name"))

    if out_directory:
        for o in result_objects:
            if convert_type == "model":
                ext = "_model.yml"
            elif convert_type == "view":
                ext = "_view.yml"
            else:
                ext = ".yml"
            with open(os.path.join(os.path.abspath(out_directory), f'{o["name"]}{ext}'), "w") as f:
                yaml.dump(o, f)
    else:
        return result_objects


@click.group()
@click.version_option()
def cli_group():
    pass


@cli_group.command()
@click.option("--directory", default=None, help="The directory of the LookML project to use in conversion")
@click.option("--out-directory", default=None, help="The the directory to write the ZenML files to")
@click.argument("path")
def view(path: str, directory: str, out_directory: str):
    """Convert a LookML view to a ZenML view with no other context"""
    result_objects = _convert_logic(path, directory, out_directory, convert_type="view")

    if result_objects:
        click.echo("\n\n".join([json.dumps(o) for o in result_objects]))


@cli_group.command()
@click.option("--directory", default=None, help="The directory of the LookML project to use in conversion")
@click.option("--out-directory", default=None, help="The the directory to write the ZenML files to")
@click.argument("path")
def model(path: str, directory: str, out_directory: str):
    """Convert a LookML model to a ZenML view with no other context"""
    result_objects = _convert_logic(path, directory, out_directory, convert_type="model")
    if result_objects:
        click.echo("\n\n".join([json.dumps(o) for o in result_objects]))


@cli_group.command()
@click.option("--directory", default=None, help="The directory of the LookML project to use in conversion")
@click.option("--out-directory", default=None, help="The the directory to write the ZenML files to")
@click.argument("path")
def dashboard(path: str, directory: str, out_directory: str):
    """Convert a LookML dashboard to a ZenML view with context from the project"""
    result_objects = _convert_logic(path, directory, out_directory, convert_type="dashboard")
    if result_objects:
        click.echo("\n\n".join([json.dumps(o) for o in result_objects]))


@cli_group.command()
@click.option("--out_directory", default=None, help="The the directory to write the ZenML files to")
@click.argument("directory")
def convert(directory: str, out_directory: str):
    """Convert a LookML dashboard to a ZenML view with context from the project"""
    if not out_directory:
        raise ValueError("--out-directory is a required option")
    project = LookMLProject(in_directory=directory, out_directory=out_directory)
    project.convert()
    click.echo(f"Project converted and saved to {out_directory}")


if __name__ == "__main__":
    cli_group()
