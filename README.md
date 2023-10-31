# LookML to ZenML

Library for translating LookML configuration into ZenML for easy onboarding to Zenlytic.

To install the package run 

```
$ pip install lookml-zenml
```

To convert a entire project run the following command from your command line interface after installing the package. Note: make sure you specify your LookML project as the first argument, and you create a directory for the ZenML output.

```
$ lookml_zenml convert ./my_lookml_project --out-directory ./my_new_zenml_project
```

This is the standard way to convert a LookML project. This will convert dashboards, views, and models into the ZenML equivalent.


---


You can also use this library to convert objects on a one-off basis. This is not as robust as converting the whole project due to loss of information for the dashboards and logic about joins in found in the explores that we add to the views. 


To convert a model run the following command. Note: if you specify `--out-directory` the library will write a yml file to that directory, otherwise it will return the converted code to stdout.

```
$ lookml_zenml model ./my_lookml_project/my_model.model.lkml --out-directory ./my_new_dir
```


To convert a view run the following command. Note: if you specify `--out-directory` the library will write a yml file to that directory, otherwise it will return the converted code to stdout.

```
$ lookml_zenml view ./my_lookml_project/my_view.view.lkml --out-directory ./my_new_dir
```

To convert a dashboard run this command. Note: for dashboards the directory is required. If you do not have the directory of lookml files, you can point to an empty directory and the conversion will run, but will put all metrics on a dashboard into the `slice_by` heading because it will be unable to determine the field type of the fields. You'll then have to correct those manually.

```
$ lookml_zenml dashboard ./my_lookml_project/my_dashboard.dashboard.lookml --directory ./my_lookml_project
```
