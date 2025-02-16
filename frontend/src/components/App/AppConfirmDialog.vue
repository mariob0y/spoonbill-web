<template>
    <v-dialog v-model="dialog" width="560" persistent>
        <v-card>
            <v-card-text class="pa-0">
                <v-row no-gutters>
                    <v-col cols="1">
                        <v-img height="24" width="24" :src="options.icon" />
                    </v-col>
                    <v-col cols="11">
                        <h3 v-if="options.title" class="pt-1 mb-6 card-title">{{ options.title }}</h3>
                        <p class="card-content">{{ options.content }}</p>
                    </v-col>
                </v-row>
            </v-card-text>

            <v-card-actions class="pa-0 mt-9">
                <v-spacer></v-spacer>
                <v-btn color="gray-light" large @click="cancel">
                    <translate>Cancel</translate>
                </v-btn>
                <v-btn class="ml-4" color="accent" large @click="confirm">
                    <v-img class="mr-2" src="@/assets/icons/arrow-in-circle.svg" />
                    {{ options.submitBtnText }}
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
    name: 'AppConfirmDialog',

    data() {
        return {
            dialog: false,
            resolve: null,
            options: {
                title: '',
                content: '',
                submitBtnText: '',
                icon: '',
            },
            defaultOptions: {
                title: this.$gettext('Are you sure to go back?'),
                content: this.$gettext('When going to the previous step, all current changes will be reversed'),
                submitBtnText: this.$gettext('Yes, go back'),
                icon: require('@/assets/icons/back.svg'),
            },
        };
    },

    created() {
        this.$root.openConfirmDialog = this.open;
    },

    methods: {
        /**
         * Opens dialog. Returns promise which allows to handle result of dialog closing
         * @return { Promise }
         */
        open(options) {
            const { title, content, submitBtnText, icon } = options || this.defaultOptions;
            this.options.title = title;
            this.options.content = content;
            this.options.submitBtnText = submitBtnText;
            this.options.icon = icon;
            this.dialog = true;

            return new Promise((resolve) => {
                this.resolve = resolve;
            });
        },

        /**
         * Handles click on 'cancel' button. Closes dialog with 'false' result
         */
        cancel() {
            this.resolve(false);
            this.dialog = false;
        },

        /**
         * Handles click on 'confirm' button. Closes dialog with 'true' result
         */
        confirm() {
            this.resolve(true);
            this.dialog = false;
        },
    },
};
</script>

<style scoped lang="scss">
.v-card {
    padding: 36px;
    .card-title {
        font-size: 24px;
        font-weight: 400;
    }
    .card-content {
        font-size: 16px;
        color: map-get($colors, 'primary');
        font-weight: 300;
        line-height: 24px;
    }
}
</style>
