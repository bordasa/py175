request_line = 'GET /?rolls=2&sides=6 HTTP/1.1'
http_method, full_path, htttp_version = request_line.split()
    
if '?' in full_path:
    path = full_path[: full_path.index('?')]
    params_str = full_path[full_path.index('?')+1: ]
    
else:
    path = full_path

key_value_pairs = params_str.split('&')
# print(key_value_pairs)
params = {key: value for key, value in
          [pair.split('=') for pair in key_value_pairs]}
        #   for key, value in pair.split('=')}

print(params)