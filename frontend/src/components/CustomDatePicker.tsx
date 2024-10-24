import { ja } from 'date-fns/locale';
import DatePicker, { registerLocale } from 'react-datepicker';
import styles from '@/styles/CustomDatePicker.module.css';

const jaLocale = {
  ...ja,
  options: { ...ja.options },
};

registerLocale('ja', jaLocale);

type Props = {
  selectedTime: Date;
  handleChange: (date: Date) => void;
  timeIntervals?: number;
};

export const CustomDatePicker = (props: Props) => {
  const { selectedTime, timeIntervals, handleChange } = props;

  return (
    <DatePicker
      dateFormat="yyyy/MM/dd HH:mm"
      locale="ja"
      selected={selectedTime}
      showTimeSelect
      timeIntervals={timeIntervals || 30}
      onChange={(date) => handleChange(date!)}
      popperPlacement="bottom-start"
      className='appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"'
      calendarClassName={styles.customCalendar}
      minTime={new Date(0, 0, 0, 8)}
      maxTime={new Date(0, 0, 0, 21)}
    />
  );
};
