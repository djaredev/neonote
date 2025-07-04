import { notify } from "$lib/state/notify.svelte";
import type { HttpValidationError } from "@neonote/sdk";

export const isHttpValidationError = (error: unknown): boolean => {
	return (
		typeof error === "object" &&
		error !== null &&
		"detail" in error &&
		Array.isArray((error as any).detail)
	);
};

export const handleError = (error: unknown) => {
	if (isHttpValidationError(error)) {
		const validationError = error as HttpValidationError;
		validationError.detail?.forEach((item) => {
			const field = item.loc[1].toString();
			notify.error(`${field}: ${item.msg}`);
		});
	}
};
