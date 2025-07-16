import type { ClientInit, HandleClientError } from "@sveltejs/kit";
import { setUpSDKClient } from "$lib/utils/sdk-client";

export const init: ClientInit = async () => {
	setUpSDKClient();
};

export const handleError: HandleClientError = ({ error, event, status, message }) => {
	return {
		message: "Something went wrong. Please try again."
	};
};
