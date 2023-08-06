from flask import Flask
from flask.globals import _request_ctx_stack
from werkzeug.exceptions import HTTPException as WerkzeugHTTPException

from .openapi import _OpenAPIMixin
from .errors import HTTPError, default_error_handler
from .scaffold import Scaffold


class APIFlask(Flask, Scaffold, _OpenAPIMixin):
    """
    The Flask object with some Web API support.

    :param import_name: the name of the application package.
    :param title: The title of the API, defaults to "APIFlask".
        You can change it to the name of your API (e.g. "Pet API").
    :param version: The version of the API, defaults to "1.0.0".
    :param tags: The tags of the OpenAPI spec documentation, accepts a list.
        See :attr:`tags` for more details.
    :param spec_path: The path to OpenAPI Spec documentation. It
        defaults to ``/openapi.json```, if the path end with ``.yaml``
        or ``.yml``, the YAML format of the OAS will be returned.
    :param swagger_path: The path to Swagger UI documentation.
    :param redoc_path: The path to Redoc documentation.
    :param json_errors: If True, APIFlask will return a JSON response
        for HTTP errors.
    :param enable_openapi: If False, will disable OpenAPI spec and docs views.
    """

    def __init__(
        self,
        import_name,
        title='APIFlask',
        version='0.1.0',
        spec_path='/openapi.json',
        docs_path='/docs',
        docs_oauth2_redirect_path='/docs/oauth2-redirect',
        redoc_path='/redoc',
        json_errors=True,
        enable_openapi=True,
        static_url_path=None,
        static_folder='static',
        static_host=None,
        host_matching=False,
        subdomain_matching=False,
        template_folder='templates',
        instance_path=None,
        instance_relative_config=False,
        root_path=None
    ):
        super(APIFlask, self).__init__(
            import_name,
            static_url_path=static_url_path,
            static_folder=static_folder,
            static_host=static_host,
            host_matching=host_matching,
            subdomain_matching=subdomain_matching,
            template_folder=template_folder,
            instance_path=instance_path,
            instance_relative_config=instance_relative_config,
            root_path=root_path
        )
        _OpenAPIMixin.__init__(
            self,
            title=title,
            version=version,
            spec_path=spec_path,
            docs_path=docs_path,
            docs_oauth2_redirect_path=docs_oauth2_redirect_path,
            redoc_path=redoc_path,
            enable_openapi=enable_openapi
        )

        # Set default config
        self.config.from_object('apiflask.settings')
        self.json_errors = json_errors
        self.spec_callback = None
        self.error_callback = default_error_handler
        self._spec = None
        self._register_openapi_blueprint()

        @self.errorhandler(HTTPError)
        def handle_http_error(error):
            return self.error_callback(
                error.status_code,
                error.message,
                error.detail,
                error.headers
            )

        if self.json_errors:
            @self.errorhandler(WerkzeugHTTPException)
            def handle_werkzeug_errrors(error):
                return self.error_callback(
                    error.code,
                    error.name,
                    detail=None,
                    headers=None
                )

    def dispatch_request(self):
        """Overwrite the default dispatch method to pass view arguments as positional
        arguments. With this overwrite, the view function can accept the parameters in
        a intuitive way (from top to bottom, from left to right)::

            @app.get('/pets/<name>/<int:pet_id>/<age>')  # -> name, pet_id, age
            @input(QuerySchema)  # -> query
            @output(PetSchema)  # -> pet
            def get_pet(name, pet_id, age, query, pet):
                pass

        From Flask, see NOTICE file for license informaiton.

        .. versionadded:: 0.2.0
        """
        req = _request_ctx_stack.top.request
        if req.routing_exception is not None:
            self.raise_routing_exception(req)
        rule = req.url_rule
        # if we provide automatic options for this URL and the
        # request came with the OPTIONS method, reply automatically
        if (  # pragma: no cover
            getattr(rule, "provide_automatic_options", False)
            and req.method == "OPTIONS"
        ):
            return self.make_default_options_response()  # pragma: no cover
        # otherwise dispatch to the handler for that endpoint
        return self.view_functions[rule.endpoint](*req.view_args.values())

    def error_processor(self, f):
        """Registers a error handler callback function.

        The callback function will be called when validation error hanppend when
        parse a request or an exception triggerd with exceptions.HTTPError or
        :func:`exceptions.abort`. It must accept four positional arguments (i.e.
        ``status_code, message, detail, headers``) and return a valid response::

            @app.error_processor
            def my_error_handler(status_code, message, detail, headers):
                return {
                    'status_code': status_code,
                    'message': message,
                    'detail': detail
                }, status_code, headers

        The arguments are:
        - status_code: If the error triggerd by validation error, the value will be
            400 (default) or the value you passed in config ``VALIDATION_ERROR_STATUS_CODE``.
            If the error triggerd by HTTP, it will be the status code you passed.
            Otherwise, it will be the status code set by Werkzueg when processing the request.
        - message: The error description for this error, either you passed or grab from Werkzeug.
        - detail: The detail of the error, it will be filled when validation error happaned, the
            structure will be::

                "<location>": {
                    "<field_name>": ["<error_message>", ...],
                    ...
                },
                ...

            The value of ``location`` can be ``json`` (i.e. request body) or ``query``
            (i.e. query string) depend on the palace the validation error happened.
        - headers: The value will be None unless you pass it in HTTPError or abort.

        If you want, you can rewrite the whole response body to anything you like::

            @app.errorhandler_callback
            def my_error_handler(status_code, message, detail, headers):
                return {'error_detail': detail}, status_code, headers

        However, I would recommend to keep the ``detail`` since it contains the detail
        information about the validation error.
        """
        self.error_callback = f
        return f
