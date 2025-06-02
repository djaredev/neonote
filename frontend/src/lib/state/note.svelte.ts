import { getContext, setContext } from "svelte";
import { archiveNote, trashNote, updateNote, type NotePublic } from "@neonote/sdk";

class NoteState {
	private notes: NotePublic[] = $state([]);
	constructor(notes: NotePublic[]) {
		this.notes = notes;
	}

	create = () => {};

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
}

const KEY = "id_noteState";

export const setNoteState = (notePublic: NotePublic[]): NoteState => {
	setContext(KEY, new NoteState(notePublic));
	return getNoteState();
};

export const getNoteState = (): NoteState => {
	return getContext(KEY) as NoteState;
};
