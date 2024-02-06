<template>
    <div>
        <section>
            <h1>Add new section</h1>
            <hr><br>

            <form @submit.prevent="submitSection">
                <div class="mb-3">
                    <label for="title" class="form-label">Title:</label>
                    <input type="text" name="title" v-model="sectionForm.title" class="form-control" required/>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </section>

        <br><br>

        <section>
            <h1>Board</h1>
            <hr><br>

            <!-- Section start-->
            <div v-if="sections" class="d-flex flex-row gap-3 justify-content-center">
                <div v-for="section in sections" :key="section.id">
                    <div class="card">
                        <div class="card-header bg-primary">
                            <div class="d-flex flex-row gap-3 justify-content-between align-items-center">
                                <span v-show="!section.visibleSectionEdit" class="text-white text-capitalize text-left align-center">{{ section.title }}</span>
                                <!-- Section title edit start -->
                                <form v-show="section.visibleSectionEdit" @submit.prevent="updSection(section.id); section.visibleSectionEdit=false">
                                    <label for="title-update"></label>
                                    <input class="form-control-sm mw-100" type="text" name="title-update" v-model="sectionUpdForm.title">
                                    <!-- <button class="btn btn-primary">Submit</button> -->
                                </form>
                                <!-- Section title edit end -->
                                <div class="btn-group">
                                    <button @click.prevent="section.visibleNoteAdd = !section.visibleNoteAdd" class="btn btn-success btn-sm">Add</button>
                                    <button @click.prevent="section.visibleSectionEdit = !section.visibleSectionEdit" class="btn btn-warning btn-sm">Edit</button>
                                    <button @click.prevent="delSection(section.id)" class="btn btn-danger btn-sm">Delete</button>
                                </div>
                            </div>
                        </div>

                        <!-- Note add start-->
                        <form v-if="section.visibleNoteAdd" @submit.prevent="submitNote(section.id); section.visibleNoteAdd=false">
                            <div class="p-3">
                                <label for="title" class="form-label">Title: </label>
                                <input required type="text" name="title" class="form-control" v-model="noteForm.title">
                                <label for="description" class="form-label">Description: </label>
                                <input type="text" name="description" class="form-control" v-model="noteForm.description">
                                <label for="comments" class="form-label">Comments: </label>
                                <input type="textarea" name="comments" class="form-control" v-model="noteForm.comments">
                                <label for="deadline" class="form-label">Deadline: </label>
                                <input required type="date" name="deadline" class="form-control" v-model="noteForm.deadline">
                            </div>
                            <button type="submit" class="btn btn-primary">Submit</button>
                        </form>
                        <!-- Note add end-->

                        <!-- Note start-->
                        <ul class="card-body">
                            <div v-if="section.note.length > 0">
                                <div v-for="note in section.note" :key="note.id" class="card mb-3">
                                    <ul class="list-group">
                                        <li class="list-group-item bg-info text-white text-capitalize text-left" @click.prevent="note.show = !note.show">{{ note.title }}
                                            <div class="btn-group">
                                                <button @click.prevent="note.visibleNoteEdit = !note.visibleNoteEdit" class="btn btn-warning btn-sm">Edit</button>
                                                <button @click.prevent="delNote(note.id)" class="btn btn-danger btn-sm">Delete</button>
                                            </div>
                                        </li>

                                        <!-- Note edit start-->
                                        <form v-if="note.visibleNoteEdit" @submit.prevent="updNote(note.id); note.visibleNoteEdit=false">
                                            <div class="p-3">
                                                <label for="title" class="form-label">Title: </label>
                                                <input required type="text" name="title" class="form-control" v-model="noteUpdForm.title">
                                                <label for="status" class="form-label">Status: </label>
                                                <select required name="status" class="form-control" v-model="noteUpdForm.section_id">
                                                    <option selected></option>
                                                    <option v-for="section in sections" :key="section.id" :value=section.id>{{ section.title }}</option>
                                                </select>
                                                <label for="description" class="form-label">Description: </label>
                                                <input type="text" name="description" class="form-control" v-model="noteUpdForm.description">
                                                <label for="comments" class="form-label">Comments: </label>
                                                <input type="textarea" name="comments" class="form-control" v-model="noteUpdForm.comments">
                                                <label for="deadline" class="form-label">Deadline: </label>
                                                <input type="date" name="deadline" class="form-control" v-model="noteUpdForm.deadline" required>
                                            </div>
                                            <button type="submit" class="btn btn-primary">Submit</button>
                                        </form>
                                        <!-- Note edit end-->

                                        <li v-if="note.description" v-show="note.show" class="list-group-item bg-light">
                                            <span class="text-left font-weight-bold">Description: </span>{{ note.description }}
                                        </li>
                                        <li v-if="note.comments" v-show="note.show" class="list-group-item bg-light">
                                            <span class="text-left font-weight-bold">Comments: </span>{{ note.comments }}
                                        </li>
                                        <li v-show="note.show" class="list-group-item bg-light">
                                            <span class="text-left font-weight-bold">Deadline: </span>{{ note.deadline }}
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div v-else>
                                <p>There is no notes.</p>
                            </div>
                        </ul>
                        <!-- Note end-->

                    </div>
                </div>
            </div>
            <div v-else>
                <p>Nothing to see here.</p>
            </div>
            <!-- Section end-->

        </section>
    </div>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
    name: "Board",
    data() {
        return {
            sectionForm: {
                title: "",
            },
            sectionUpdForm: {
                title: "",
            },
            noteForm: {
                title: "",
                description: "",
                comments: "",
                deadline: Date(""),
                section_id: 0
            },
            noteUpdForm: {
                title: this.title,
                description: this.description,
                comments: "",
                deadline: Date(""),
                section_id: 0
            },
        }
    },
    created: function() {
        return this.$store.dispatch("getSections")
    },
    computed: {
        ...mapGetters({sections: "stateSections", notes: "stateNotes"})
    },
    methods: {
        ...mapActions(["createSection"]),
        ...mapActions(["updateSection"]),
        ...mapActions(["deleteSection"]),
        ...mapActions(["createNote"]),
        ...mapActions(["updateNote"]),
        ...mapActions(["deleteNote"]),
        async submitSection() {
            await this.createSection(this.sectionForm)
        },
        async updSection(section_id) {
            let section = {
                form: this.sectionUpdForm, 
                id: section_id
            }
            await this.updateSection(section)
            return this.$store.dispatch("getSections")
        },
        async delSection(section_id) {
            await this.deleteSection(section_id)
            return this.$store.dispatch("getSections")
        },
        async submitNote(section_id) {
            this.noteForm["section_id"] = section_id
            await this.createNote(this.noteForm)
            return this.$store.dispatch("getSections")
        },
        async updNote(note_id) {
            let note = {
                form: this.noteUpdForm, 
                id: note_id
            }
            await this.updateNote(note)
            return this.$store.dispatch("getSections")
        },
        async delNote(note_id) {
            await this.deleteNote(note_id)
            return this.$store.dispatch("getSections")
        },
    }
})
</script>