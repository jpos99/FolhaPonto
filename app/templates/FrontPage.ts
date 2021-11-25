import { enableRipple } from '@syncfusion/ej2-base';
enableRipple(false);
import { DatePicker } from '@syncfusion/ej2-calendars';

/**
 * Range DatePicker sample
 */

let today: Date = new Date();
let currentYear: number = today.getFullYear();
let currentMonth: number = today.getMonth();

let datepicker: DatePicker = new DatePicker({
    min: new Date(currentYear, currentMonth, 7),
    max: new Date(currentYear, currentMonth, 27),
    value: new Date(currentYear, currentMonth, 14),
    placeholder: 'Select a date',
    width: "233px"
});
datepicker.appendTo('#datepicker');
datepicker.show();
