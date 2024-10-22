'use client';

import FullCalendar from '@fullcalendar/react';
import interactionPlugin from '@fullcalendar/interaction';
import dayGridPlugin from '@fullcalendar/daygrid';
import { useEffect, useState } from 'react';
import { Booking } from '@/types/booking';
import { getBookingsSummaries } from '@/api/booking';

// 3台分の色を定義
const EVENT_COLORS = ['#4169e1', '#ff6347', '#008000'];

export default function Calendar() {
  const [bookings, setBookings] = useState(undefined);

  useEffect(() => {
    const fetchBookings = async () => {
      const response = await getBookingsSummaries();

      // 車両名を重複なしで取得
      const carNames = Array.from(
        new Set(response.map((booking: Booking) => booking.car.name))
      );

      setBookings(
        response.map((booking: Booking) => ({
          title: booking.car.name,
          start: booking.startTime.slice(0, 10),
          end: booking.endTime.slice(0, 10),
          color: EVENT_COLORS[carNames.indexOf(booking.car.name) % 3],
        }))
      );
    };

    fetchBookings();
  }, []);

  return (
    <FullCalendar
      locale="ja"
      plugins={[dayGridPlugin, interactionPlugin]}
      initialView="dayGridMonth"
      selectable={true}
      events={bookings}
    />
  );
}
