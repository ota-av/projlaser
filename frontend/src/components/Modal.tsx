import { useEffect, useState, PropsWithChildren } from "react";
import { XMarkIcon } from "@heroicons/react/20/solid";

interface ModalProps extends PropsWithChildren {
  open: boolean;
  onClose: () => void;
}

// A popup window
export default function Modal({ children, open, onClose }: ModalProps) {
  return (
    <div
      className={`fixed z-10 bg-black/40 top-0 left-0 w-full h-full transition duration-100 flex justify-center items-center ${
        open ? "opacity-100" : "opacity-0 hidden"
      }`}
      onClick={onClose}
    >
      <div
        className={`relative z-20 bg-white transition duration-100 flex-grow p-4 rounded text-gray-800 m-10 max-h-[75%] overflow-hidden flex flex-col ${
          open ? "opacity-100" : "opacity-0 hidden"
        }`}
        onClick={(e) => e.stopPropagation()}
      >
        <button
          className="absolute top-2 right-2 hover:bg-neutral-200 p-1 rounded-full transition duration-100"
          onClick={onClose}
        >
          <XMarkIcon className="w-6 h-6 text-gray-800 hover:text-gray-900 transition duration-100" />
        </button>
        {children}
      </div>
    </div>
  );
}
