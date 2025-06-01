import { getContext, setContext } from "svelte";
import { updateNote, type NotePublic } from "@neonote/sdk";

class NoteState {
	// private notes: NotePublic[] | null = $state(null);
	private notes: NotePublic[] = $state([]);
	constructor(notes: NotePublic[]) {
		this.notes = notes;
	}

	create = () => {};

	findById = (id: string): NotePublic | undefined => {
		return this.notes?.find((n) => n.id === id);
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

	remove = () => {};
}

const KEY = "id_noteState";

export const setNoteState = (notePublic: NotePublic[]): NoteState => {
	setContext(KEY, new NoteState(notePublic));
	return getNoteState();
};

export const getNoteState = (): NoteState => {
	return getContext(KEY) as NoteState;
};
