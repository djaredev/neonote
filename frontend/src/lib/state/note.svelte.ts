import { getContext, setContext } from "svelte";
import { NotificationLayout, notify } from "./notify.svelte";
import {
	archiveNote,
	createNote,
	deleteNote,
	restoreNote,
	trashNote,
	unarchiveNote,
	updateNote,
	type NoteCreate,
	type NotePublic
} from "@neonote/sdk";

const success = (ms: string) => {
	notify.success({
		title: ms,
		layoutType: NotificationLayout.Minimal
	});
};

const error = (ms: string) => {
	notify.error({
		title: ms,
		layoutType: NotificationLayout.Minimal
	});
};

class NoteState {
	notes: NotePublic[] = $state([]);
	constructor(notes: NotePublic[]) {
		this.notes = notes;
	}

	set(notes: NotePublic[]) {
		this.notes = notes;
	}

	create = async (note: NoteCreate) => {
		if (note.title === "" || note.content === "") return;
		const res = await createNote({ body: note });
		if (res.data) {
			this.notes.unshift(res.data);
			console.log(this.notes.length);
			success("Note created");
		}
	};

	findById = (id: string): NotePublic | undefined => {
		const note = this.notes.find((n) => n.id === id);
		if (note) {
			return note;
		}
		error("Note not found");
		return undefined;
	};

	getAll = () => {
		return this.notes;
	};

	update = async (noteSnapshot: NotePublic) => {
		const note = this.findById(noteSnapshot.id);
		if (note && (note.title !== noteSnapshot.title || note.content !== noteSnapshot.content)) {
			const res = await updateNote({
				body: {
					title: note.title,
					content: note.content
				},
				path: {
					id: note.id
				}
			});
			success("Note updated");
			return res;
		}
	};

	delete = async (id: string) => {
		const res = await deleteNote({ path: { id: id } });
		if (res.data) {
			this.notes = this.notes.filter((n) => n.id !== id);
			success("Note deleted");
		}
	};

	archive = async (id: string) => {
		const res = await archiveNote({
			path: {
				id
			}
		});
		if (res.response.status === 204) {
			this.notes = this.notes.filter((n) => n.id !== id);
			success("Note archived");
		}
	};

	unArchive = async (id: string) => {
		const res = await unarchiveNote({
			path: {
				id
			}
		});
		if (res.response.status === 204) {
			this.notes = this.notes.filter((n) => n.id !== id);
			success("Note unarchived");
		}
	};

	trash = async (id: string) => {
		const res = await trashNote({
			path: {
				id
			}
		});
		if (res.response.status === 204) {
			this.notes = this.notes.filter((n) => n.id !== id);
			success("Note trashed");
		}
	};

	restore = async (id: string) => {
		const res = await restoreNote({
			path: {
				id
			}
		});
		if (res.response.status === 204) {
			this.notes = this.notes.filter((n) => n.id !== id);
			success("Note restored");
		}
	};
}

const KEY = "id_noteState";

export const setNoteState = (notePublic: NotePublic[]): NoteState => {
	setContext(KEY, new NoteState(notePublic));
	return getNoteState();
};

export const getNoteState = (): NoteState => {
	return getContext(KEY) as NoteState;
};
