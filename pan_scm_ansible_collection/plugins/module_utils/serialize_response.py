def serialize_response(response):
    """Convert response to Ansible-compatible format."""
    if hasattr(response, 'model_dump'):
        data = response.model_dump()
        # Convert UUID to string
        if 'id' in data and data['id']:
            data['id'] = str(data['id'])
        return data
    return response
