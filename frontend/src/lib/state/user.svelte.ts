import { whoami, type UserPublic } from "@neonote/sdk";

const user: UserPublic = $state({
	username: "",
	email: ""
});

export const setUser = (usr: UserPublic): void => {
	user.username = usr.username;
	user.email = usr.email;
};

export const getUser = (): UserPublic => {
	return user;
};
