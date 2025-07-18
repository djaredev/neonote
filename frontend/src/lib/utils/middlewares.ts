import { notify } from "$lib/state/notify.svelte";
import type { HttpValidationError } from "@neonote/sdk";

type HttpError = {
	detail: string;
};

export const isHttpValidationError = (error: unknown): boolean => {
	return (
		typeof error === "object" &&
		error !== null &&
		"detail" in error &&
		Array.isArray((error as any).detail)
	);
};

export const isHttpError = (error: unknown): boolean => {
	return (
		typeof error === "object" &&
		error !== null &&
		"detail" in error &&
		typeof (error as HttpError).detail === "string"
	);
};

export const handleHttpError = (error: unknown) => {
	if (isHttpValidationError(error)) {
		const validationError = error as HttpValidationError;
		validationError.detail?.forEach((item) => {
			const field = item.loc[1].toString();
			notify.error(`${field}: ${item.msg}`);
		});
		return;
	}

	if (isHttpError(error)) {
		const httpError = error as HttpError;
		notify.error(httpError.detail);
		return;
	}

	notify.error("Something went wrong. Please try again.");
};

export const handleError = (error: unknown) => {
	if (error instanceof TypeError) {
		notify.error("Could not connect to server. Check your internet connection.");
		return;
	}
	notify.error("Something went wrong. Please try again.");
};
