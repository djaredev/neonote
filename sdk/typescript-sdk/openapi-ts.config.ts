import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "http://127.0.0.1:8000/openapi.json",
  output: "src/client",
  plugins: [
    {
      name: "@hey-api/client-fetch",
      runtimeConfigPath: "./src/custom-client.ts",
    },
    "zod",
    {
      name: "@hey-api/sdk",
      // @ts-ignore
      methodNameBuilder: (operation) => {
        let name = operation.id;
        if (name) {
          name = name.replace(
            new RegExp(operation.path.slice(1) + operation.method, "i"),
            "",
          );
        }
        return name;
      },
    },
    {
      name: "@hey-api/schemas",
      type: "json",
    },
  ],
});
