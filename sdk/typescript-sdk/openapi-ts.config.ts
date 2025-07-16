import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "../openapi.json",
  output: "src/client",
  plugins: [
    {
      name: "@hey-api/client-fetch",
      runtimeConfigPath: "./src/custom-client.ts",
    },
    // "zod",
    {
      name: "@hey-api/sdk",
      // @ts-ignore
      methodNameBuilder: (operation) => {
        console.log(operation);
        let summary = operation.summary;
        if (summary) {
          summary = (summary.charAt(0).toLowerCase() + summary.slice(1))
            .split(" ")
            .join("");
        }
        return summary;
      },
    },
    {
      name: "@hey-api/schemas",
      type: "json",
    },
  ],
});
