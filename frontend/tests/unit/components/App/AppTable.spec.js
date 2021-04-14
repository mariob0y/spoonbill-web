import { mount } from '@vue/test-utils';
import AppTable from '@/components/App/AppTable';

describe('AppTable.vue', () => {
    test("'highlightedCols' returns indexes of additional columns", () => {
        const wrapper = mount(AppTable, {
            propsData: {
                name: 'Test',
                headers: ['h1', 'h2', 'h3', 'h4', 'h5'],
                data: [['d1', 'd2', 'd3', 'd4', 'd5']],
                additionalColumns: ['h2', 'h3'],
            },
        });

        expect(wrapper.vm.highlightedCols).toStrictEqual([1, 2]);
    });

    describe('methods', () => {
        test("'changeName' emits 'change-name' event with entered value", () => {
            const wrapper = mount(AppTable, {
                propsData: {
                    name: 'Test',
                    headers: ['h1', 'h2', 'h3', 'h4', 'h5'],
                    data: [['d1', 'd2', 'd3', 'd4', 'd5']],
                    additionalColumns: ['h2', 'h3'],
                },
            });

            wrapper.setData({
                newName: 'new name',
            });
            wrapper.vm.changeName();
            expect(wrapper.emitted()['change-name']).toStrictEqual([['new name']]);
            expect(wrapper.vm.nameMenu).toBe(false);
        });
    });

    describe('watchers', () => {
        test("'nameMenu' updates 'newName' value", async () => {
            const wrapper = mount(AppTable, {
                propsData: {
                    name: 'Test',
                    headers: ['h1', 'h2', 'h3', 'h4', 'h5'],
                    data: [['d1', 'd2', 'd3', 'd4', 'd5']],
                    additionalColumns: ['h2', 'h3'],
                },
            });

            await wrapper.setData({
                newName: null,
                nameMenu: true,
            });
            expect(wrapper.vm.newName).toBe('Test');
        });
    });
});
