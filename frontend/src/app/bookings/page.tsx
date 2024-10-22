import BookingForm from '@/features/booking/components/BookingForm';
import Calendar from '@/features/booking/components/Calendar';

export default function Page() {
  return (
    <div>
      <div className="m-10 max-w-xl">
        <Calendar />
      </div>
      <div className="m-10">
        <BookingForm />
      </div>
    </div>
  );
}
