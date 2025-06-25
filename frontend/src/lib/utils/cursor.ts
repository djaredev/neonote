export const createCursor = (id: string, createdAt: string): string => {
	const base64 = btoa(
		JSON.stringify({
			id: id,
			created_at: createdAt
		})
	);
	return base64.replace(/\+/g, "-").replace(/\//g, "_");
};
