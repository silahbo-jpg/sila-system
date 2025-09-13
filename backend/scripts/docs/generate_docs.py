"""Generate API documentation from FastAPI app."""
import os
import re
from typing import Dict, Any, List, Optional

from fastapi import FastAPI
from fastapi.routing import APIRoute

class APIDocGenerator:
    """Generate HTML documentation for FastAPI endpoints."""
    
    def __init__(self, app: FastAPI, title: str = "API Documentation"):
        """Initialize with FastAPI app instance."""
        self.app = app
        self.title = title
        
    def _get_method_color(self, method: str) -> str:
        """Return Bootstrap color class based on HTTP method."""
        method_colors = {
            'get': 'success',
            'post': 'primary',
            'put': 'warning',
            'delete': 'danger',
            'patch': 'info',
            'options': 'secondary',
            'head': 'dark'
        }
        return method_colors.get(method.lower(), 'secondary')
    
    def _get_endpoint_details(self, route: APIRoute) -> Dict[str, Any]:
        """Extract endpoint details from route."""
        path = route.path
        methods = route.methods
        summary = route.summary or ''
        description = route.description or ''
        operation_id = route.operation_id
        
        # Extract parameters from path and OpenAPI schema
        parameters = []
        path_params = re.findall(r'{([^}]+)}', path)
        
        for param in path_params:
            parameters.append({
                'name': param,
                'in': 'path',
                'required': True,
                'schema': {'type': 'string'}
            })
        
        # Get additional parameters from OpenAPI schema
        if hasattr(route, 'openapi_extra') and route.openapi_extra:
            if 'parameters' in route.openapi_extra:
                parameters.extend(route.openapi_extra['parameters'])
        
        # Get request body if available
        request_body = None
        if route.body_field:
            request_body = {
                'description': route.body_field.field_info.description or '',
                'required': route.body_field.required,
                'content': {
                    'application/json': {
                        'schema': route.body_field.type_.__name__
                    }
                }
            }
        
        # Get responses
        responses = {}
        if hasattr(route, 'responses') and route.responses:
            for status_code, response in route.responses.items():
                responses[status_code] = {
                    'description': response.get('description', ''),
                    'content': response.get('content', {})
                }
        else:
            # Default 200 response
            responses['200'] = {
                'description': 'Successful response',
                'content': {}
            }
        
        return {
            'path': path,
            'methods': methods,
            'summary': summary,
            'description': description,
            'operation_id': operation_id,
            'parameters': parameters,
            'request_body': request_body,
            'responses': responses
        }
    
    def _generate_endpoint_html(self, method: str, path: str, details: Dict[str, Any]) -> str:
        """Generate HTML for a single endpoint."""
        method_class = method.lower()
        summary = details['summary']
        description = details['description']
        
        # Generate parameters HTML
        parameters_html = ""
        if details['parameters']:
            param_items = []
            for param in details['parameters']:
                param_type = param.get('in', 'query')
                required = 'required' if param.get('required', False) else 'optional'
                param_items.append(
                    f"<li><code>{param['name']}</code> <span class='badge bg-secondary me-1'>{param_type}</span> "
                    f"<span class='badge bg-{'danger' if required == 'required' else 'light text-dark'}'>{required}</span> "
                    f"<small class='text-muted'>{param.get('description', '')}</small></li>"
                )
            
            if param_items:
                parameters_html = f"<h6 class='mt-3'>Parâmetros:</h6><ul class='list-unstyled'>{' '.join(param_items)}</ul>"
        
        # Generate request body HTML
        if details['request_body']:
            body_required = 'required' if details['request_body'].get('required', False) else 'optional'
            body_schema = next(iter(details['request_body']['content'].values())).get('schema', '')
            
            body_html = (
                f"<h6 class='mt-3'>Request Body:</h6>"
                f"<div class='ms-3'>"
                f"<span class='badge bg-{'danger' if body_required == 'required' else 'light text-dark'}'>{body_required}</span> "
                f"<small class='text-muted'>{details['request_body'].get('description', '')}</small>"
                f"<div><code>{body_schema}</code></div>"
                f"</div>"
            )
            parameters_html += body_html
        
        # Generate responses HTML
        responses_html = ""
        if details['responses']:
            responses = []
            for status_code, response in details['responses'].items():
                badge_color = 'success' if status_code.startswith('2') else 'danger'
                response_item = f"<li><span class='badge bg-{badge_color} me-2'>{status_code}</span> {response.get('description', '')}</li>"
                responses.append(response_item)
            
            if responses:
                responses_html = f"<h6 class='mt-3'>Respostas:</h6><ul class='list-unstyled'>{''.join(responses)}</ul>"
        
        return f"""
        <div class="endpoint {method_class} mb-4 p-3 bg-light">
            <div class="d-flex justify-content-between align-items-center">
                <h4><span class="badge bg-{self._get_method_color(method)}">{method.upper()}</span> {path}</h4>
                <span class="text-muted">{summary}</span>
            </div>
            {f'<p class="mt-2">{description}</p>' if description else ''}
            {parameters_html}
            {responses_html}
        </div>
        """
    
    def generate_html(self) -> str:
        """Generate complete HTML documentation."""
        endpoints_by_tag = {}
        
        # Group endpoints by tag
        for route in self.app.routes:
            if isinstance(route, APIRoute):
                for method in route.methods:
                    if method not in ['HEAD', 'OPTIONS']:
                        details = self._get_endpoint_details(route)
                        
                        # Get tags from route
                        tags = getattr(route, 'tags', ['default'])
                        if not tags:
                            tags = ['default']
                            
                        for tag in tags:
                            if tag not in endpoints_by_tag:
                                endpoints_by_tag[tag] = []
                            
                            endpoints_by_tag[tag].append({
                                'method': method,
                                'path': route.path,
                                'details': details
                            })
        
        # Generate HTML for each tag
        sections_html = []
        for tag, endpoints in sorted(endpoints_by_tag.items()):
            endpoints_html = []
            for endpoint in sorted(endpoints, key=lambda x: x['path']):
                endpoints_html.append(
                    self._generate_endpoint_html(
                        endpoint['method'],
                        endpoint['path'],
                        endpoint['details']
                    )
                )
            
            sections_html.append(f"""
            <div class="tag-section mb-5">
                <h2 class="mb-3">{tag}</h2>
                {''.join(endpoints_html)}
            </div>
            """)
        
        # Complete HTML document
        return f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.title}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ padding-top: 2rem; padding-bottom: 2rem; }}
                .endpoint {{ border-radius: 0.25rem; }}
                .get {{ border-left: 4px solid #28a745; }}
                .post {{ border-left: 4px solid #007bff; }}
                .put {{ border-left: 4px solid #ffc107; }}
                .delete {{ border-left: 4px solid #dc3545; }}
                .patch {{ border-left: 4px solid #17a2b8; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="mb-4">{self.title}</h1>
                {''.join(sections_html)}
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """

def generate_api_docs(app: FastAPI, output_file: str, title: str = "API Documentation"):
    """Generate API documentation and save to file."""
    generator = APIDocGenerator(app, title)
    html_content = generator.generate_html()
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"API documentation generated at {output_file}")

