import React from "react";
import "./App.css";
import "./accordion.css";
import {
	Accordion,
	AccordionItem,
	AccordionItemHeading,
	AccordionItemButton,
	AccordionItemPanel,
} from "react-accessible-accordion";
import "react-accessible-accordion/dist/fancy-example.css";

class App extends React.Component<
	{},
	{
		tube: {
			[key: string]: {
				affected_stations: string[];
				details: string | null;
				line: string;
				status: string;
			};
		};
		update: string;
	}
> {
	interval: any;
	constructor(props: {}) {
		super(props);
		this.state = {
			tube: {},
			update: this.getTime(),
		};
	}
	getData(): void {
		fetch("/underground")
			.then((res) => res.json())
			.then((res) => {
				console.log(res);
				this.setState({
					tube: res.current_status,
					update: this.getTime(),
				});
			});
	}
	getTime(): string {
		return new Date().toTimeString().split(":").splice(0,2).join(":")
	}

	componentDidMount() {
		this.getData();
		this.interval = setInterval(() => {
			this.getData();
		}, 5 * 60 * 1000);
	}
	componentWillUnmount() {
		clearInterval(this.interval);
	}
	render() {
		return (
			<div className="App">
				<h2>
					Status for the TfL network (Undergound, Overgound, Trams, Crossrail
					and DLR)
				</h2>
				<p className="time">Last updated at {this.state.update}</p>
				<hr />
				<Accordion
					style={{
						backgroundColor: "#12121211",
						padding: "0",
						textAlign: "left",
					}}
					allowZeroExpanded
				>
					{Object.keys(this.state.tube).map((k, i) => {
						let data = this.state.tube[k];
						return (
							<AccordionItem
								key={i.toString()}
								style={{
									backgroundColor: "#35353566",
								}}
							>
								<AccordionItemHeading
									style={{
										paddingBottom: "10px",
									}}
								>
									<AccordionItemButton
										style={{
											backgroundColor: "inherit",
											color: "#fff",
											cursor: "pointer",
											height: "15px",
											fontSize: "15px",
											padding: "10px 10px 10px 10px",
											/*width: 100%;
											text-align: left;
											border: none;*/
										}}
									>
										{data.line +
											([
												"DLR",
												"Trams",
												"Overground",
												"Elizabeth Line",
											].includes(data.line)
												? ""
												: " Line")}{" "}
										- {data.status}{" "}
									</AccordionItemButton>
								</AccordionItemHeading>
								<AccordionItemPanel
									style={{
										fontSize: "20px",
									}}
								>
									<p>{data.details || "Regular Service"}</p>
								</AccordionItemPanel>
							</AccordionItem>
						);
					})}
				</Accordion>
				<hr />
				<p className="time">
					<i>Updates automatically every 5 minutes</i>
					<br />
					<a href="https://github.com/cxllm/tfl-status-api">API Usage</a>
				</p>
			</div>
		);
	}
}

export default App;
