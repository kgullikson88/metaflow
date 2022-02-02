import hashlib

# def kubernetes_compatible_name(name):
# 	# Unfortunately, all Kubernetes compatible names must consist of lower case
# 	# alphanumeric characters, '-' or '.'; must start and end with an alphanumeric
# 	# character; and must be under 63 characters.
# 	#
# 	# https://github.com/kubernetes/kubernetes/issues/94088

# 	hash = hashlib.sha256(name.encode("utf-8")).hexdigest()[:15]
# 	name = "mf" + name
#     return name.replace("_", "-").lower()[:47] + "-" + hash
