# Python client for Azure Data Lake Store

Microsoft's Azure Data Lake Store can be accessed by WebHDFS - with a twist. You must add some authentication details. As we all know, *any* authentication in Azure is painful. 

The whole point of PyADL is to take care of that painful part. It will wrap `pywebhdfs` client, passing it the necessary authentication details.

You will need to add an application to Azure Active Directory, create a key for this application, delegate access to Azure Management Services, and grant it the "Contributor" role in your Azure Data Lake Store. 

If you don't know how to do that check out the "Prerequisites" section in [this article](https://github.com/Azure/azure-content/blob/master/articles/data-lake-store/data-lake-store-get-started-rest-api.md).

I'll add more documentation soon - for now the source code is about 40 lines long so just look there :).