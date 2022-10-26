generate-spec gen-spec:
	poetry run task generate:spec

generate-client-ts-axios genc-axios: gen-spec
	docker run --rm \
		--user $$(id -u):$$(id -g) \
		-v "$(dir $(abspath $(lastword $(MAKEFILE_LIST)))):/local" openapitools/openapi-generator-cli generate \
		-g typescript-axios \
		--additional-properties=supportsES6=true,npmName=${PACKAGE_NAME},npmRepository=${PACKAGE_REPOSITORY} \
		-i /local/generated/openapi.yml \
		-o /local/generated/typescript
