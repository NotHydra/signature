export default interface FormatResponse<T> {
    success: boolean,
    status: number,
    message: string,
    data: T
}