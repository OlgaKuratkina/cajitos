# from typing import Optional, Any
#
# from flask import Flask
# # from concurrent.futures import Future
#
# class ElasticClient(Elasticsearch):
#     def __init__(self, es_host: str, es_port: int, es_region: Optional[str] = None):
#         if es_region:
#             super().__init__(
#                 hosts=[{'host': es_host, 'port': es_port}],
#                 connection_class=RequestsHttpConnection,
#                 http_compress=True,
#                 timeout=25,
#                 retry_on_timeout=True,
#                 use_ssl=True,
#                 verify_certs=True
#             )
#         else:
#             super().__init__(
#                 hosts=[{'host': es_host, 'port': es_port}],
#                 connection_class=RequestsHttpConnection,
#                 http_compress=True,
#                 timeout=25,
#                 retry_on_timeout=True
#             )
#
#
# class ElasticFlaskProxy:
#     """
#     Proxy object that mimics an Elasticsearch client that can be reconfigured
#     using init_app()
#     """
#     def __init__(self, app: Optional[Flask] = None) -> None:
#         self.app = None
#         self.client = None
#         if app is not None:
#             self.init_app(app)
#
#     def init_app(self, app: Flask) -> None:
#         """
#         Create an ElasticClient instance for this app
#         """
#         self.app = app
#         self.client = ElasticClient(
#             es_host=app.config['ELASTICSEARCH_URI'],
#             es_port=int(app.config['ELASTICSEARCH_PORT']),
#             es_region=app.config.get('ELASTICSEARCH_REGION')
#         )
#
#     def __getattr__(self, attr: str) -> Any:
#         """
#         Proxy client object
#         """
#         try:
#             getattr(super(), attr)
#         except AttributeError as exc:
#             if self.client is None:
#                 raise RuntimeError('Proxy not initialized.') from exc
#             return getattr(self.client, attr)