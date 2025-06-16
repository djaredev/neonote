import { getContext, setContext } from "svelte";
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
			console.log("Note created");
			this.notes.unshift(res.data);
			console.log(this.notes.length);
		}
	};

	findById = (id: string): NotePublic | undefined => {
		return this.notes.find((n) => n.id === id);
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
			return res;
		}
	};

	delete = async (id: string) => {
		try {
			await deleteNote({ path: { id: id } });
			this.notes = this.notes.filter((n) => n.id !== id);
			console.log("Note deleted");
		} catch (error) {
			console.log("Error deleting note");
			console.log(error);
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
